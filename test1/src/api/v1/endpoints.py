from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from typing import Dict, List
import json

from src.config.settings import settings

from src.models.models import (
    ServiceStatus,
    HealthCheckResponse,
    StatusResponse
)

from src.config.logger import logger
from src.services.el_search_service import ElasticsearchServiceNew

router = APIRouter(prefix="/v1", tags=["Test1v1"])


es_service_new = ElasticsearchServiceNew(
    hosts=settings.elasticsearch_hosts,
    index_name=settings.elasticsearch_index
)


@router.post("/add", response_model=StatusResponse, status_code=201)
async def add_service_status(file: UploadFile = File(...)):

    try:
        content = await file.read()
        data = json.loads(content)            

        
        if "service_name" in data or "application_name" in data:
            result = es_service_new.index_document(data)
            
            if result["success"]:
                return StatusResponse(
                    message="Service status added successfully",
                    data=result
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to index document: {result.get('error')}"
                )
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid JSON structure. Must contain 'service_name' or 'application_name'"
            )

            
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")
    except Exception as e:
        logger.__error__(f"Error processing file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/healthcheck", response_model=HealthCheckResponse)
async def get_all_health_status():

    try:
        app_status = es_service_new.get_application_status()
        
        all_services = es_service_new.get_all_services()
        
        service_map = {}
        for service in all_services:
            name = service.get('service_name') or service.get('application_name')
            if name and name not in service_map:
                service_map[name] = service

        
        
        return HealthCheckResponse(
            status=app_status['application_status'],  
            services=[
                {
                    "name": name,
                    "status": data.get('service_status') ,
                    "host": data.get('host_name'),
                    "timestamp": data.get('timestamp')
                }
                for name, data in service_map.items()
            ]
        )
        
    except Exception as e:
        logger.__error__(f"Error getting health status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/healthcheck/{service_name}", response_model=ServiceStatus)
async def get_service_health_status(service_name: str):

    try:
        service = es_service_new.get_service_by_name(service_name)
        
        if not service:
            raise HTTPException(
                status_code=404,
                detail=f"Service '{service_name}' not found"
            )
        
        status = service.get('service_status') or service.get('application_status')
        
        return ServiceStatus(
            name=service_name,
            status=status,
            host=service.get('host_name'),
            timestamp=service.get('timestamp'),
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.__error__(f"Error getting service health: {e}")
        raise HTTPException(status_code=500, detail=str(e))
