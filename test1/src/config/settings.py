from pydantic_settings import BaseSettings
from typing import List, Dict


class Settings(BaseSettings):
    
    app_name: str = "RBC Application Monitoring API"
    app_version: str = "1.0.0"
    api_v1_prefix: str = "/api/v1"
    debug: bool = True

    host: str = "localhost"
    port: int = 9200
    elasticsearch_index: str = "service-status"

    elasticsearch_url: str = "https://af5d3188fa7a49b48315c0271fcaee48.us-central1.gcp.cloud.es.io:443"
    elasticsearch_api_key: str = "bzBCdkRwd0J0Ukt1WjhremxTcks6cWJuS0MweXZxZENaak9nWXpTMTNKdw=="
    
    application_name: str = "rbcapp1"
    
    cors_origins: List[str] = ["*"]

    services: List[str] = ["httpd", "rabbitmq-server", "postgresql"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()