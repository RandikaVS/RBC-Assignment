from datetime import datetime
from typing import List, Dict, Optional
from elasticsearch import Elasticsearch, NotFoundError
from src.config.logger import logger


class ElasticsearchServiceNew:
    
    def __init__(self, hosts: List[str], index_name: str = "service-status"):

        self.index_name = index_name
        
        try:
            self.es = Elasticsearch(
                hosts=hosts,
                verify_certs=False,
                ssl_show_warn=False
            )
            
            if self.es.ping():
                logger.__info__("Successfully connected to Elasticsearch")
                self._create_index_if_not_exists()
            else:
                logger.__warning__("Could not ping Elasticsearch - running in mock mode")
                self.es = None
                
        except Exception as e:
            logger.__warning__(f"Could not connect to Elasticsearch: {e}. Running in mock mode.")
            self.es = None
            
        self.mock_storage: List[Dict] = []
    
    def _create_index_if_not_exists(self):
        if not self.es:
            return
            
        try:
            if not self.es.indices.exists(index=self.index_name):
                mapping = {
                    "mappings": {
                        "properties": {
                            "service_name": {"type": "keyword"},
                            "application_name": {"type": "keyword"},
                            "service_status": {"type": "keyword"},
                            "application_status": {"type": "keyword"},
                            "host_name": {"type": "keyword"},
                            "timestamp": {"type": "date"},
                            "dependent_services": {
                                "type": "nested",
                                "properties": {
                                    "service_name": {"type": "keyword"},
                                    "service_status": {"type": "keyword"},
                                    "host_name": {"type": "keyword"}
                                }
                            }
                        }
                    }
                }
                
                self.es.indices.create(index=self.index_name, body=mapping)
                logger.__info__(f"Created index: {self.index_name}")
        except Exception as e:
            logger.__error__(f"Error creating index: {e}")
    
    def index_document(self, document: Dict) -> Dict:

        if self.es:
            try:
                # Add timestamp if not present
                if 'timestamp' not in document:
                    document['timestamp'] = datetime.utcnow().isoformat() + "Z"
                
                response = self.es.index(
                    index=self.index_name,
                    document=document
                )
                logger.__info__(f"Indexed document: {response['_id']}")
                return {
                    "success": True,
                    "id": response["_id"],
                    "result": response["result"]
                }
            except Exception as e:
                logger.__error__(f"Error indexing document: {e}")
                return {"success": False, "error": str(e)}
        else:
            # Mock mode
            document['_id'] = f"mock-{len(self.mock_storage)}"
            document['timestamp'] = document.get('timestamp', datetime.utcnow().isoformat() + "Z")
            self.mock_storage.append(document)
            logger.__info__(f"[MOCK] Stored document: {document['_id']}")
            return {
                "success": True,
                "id": document['_id'],
                "result": "created",
                "mode": "mock"
            }
    
    def get_all_services(self) -> List[Dict]:

        if self.es:
            try:
                response = self.es.search(
                    index=self.index_name,
                    body={
                        "query": {"match_all": {}},
                        "sort": [{"timestamp": {"order": "desc"}}],
                        "size": 100
                    }
                )
                
                return [hit["_source"] for hit in response["hits"]["hits"]]
            except NotFoundError:
                logger.__warning__(f"Index {self.index_name} not found")
                return []
            except Exception as e:
                logger.__error__(f"Error searching documents: {e}")
                return []
        else:
            return sorted(
                self.mock_storage,
                key=lambda x: x.get('timestamp', ''),
                reverse=True
            )
    
    def get_service_by_name(self, service_name: str) -> Optional[Dict]:

        if self.es:
            try:
                response = self.es.search(
                    index=self.index_name,
                    body={
                        "query": {
                            "bool": {
                                "should": [
                                    {"match": {"service_name": service_name}},
                                    {"match": {"application_name": service_name}}
                                ]
                            }
                        },
                        "sort": [{"timestamp": {"order": "desc"}}],
                        "size": 1
                    }
                )
                
                hits = response["hits"]["hits"]
                return hits[0]["_source"] if hits else None
                
            except NotFoundError:
                logger.__warning__(f"Index {self.index_name} not found")
                return None
            except Exception as e:
                logger.__error__(f"Error searching for service {service_name}: {e}")
                return None
        else:
            matching = [
                doc for doc in self.mock_storage
                if doc.get('service_name') == service_name 
                or doc.get('application_name') == service_name
            ]
            
            if matching:
                return sorted(
                    matching,
                    key=lambda x: x.get('timestamp', ''),
                    reverse=True
                )[0]
            return None
    
    def get_application_status(self, app_name: str = "rbcapp1") -> Dict:
       
        services = ['httpd', 'rabbitmq-server', 'postgresql']
        down_services = []
        
        for service in services:
            status = self.get_service_by_name(service)
            if not status or status.get('service_status') == 'DOWN':
                down_services.append(service)
        
        app_status = "DOWN" if down_services else "UP"
        
        return {
            "application_name": app_name,
            "application_status": app_status,
            "down_services": down_services,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }