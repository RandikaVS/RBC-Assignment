
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class ServiceStatus(BaseModel):
    name: str = Field(..., description="Name of the service")
    status: str = Field(..., pattern="^(UP|DOWN)$", description="Status of the service")
    host: str = Field(..., description="Hostname where service runs")
    timestamp: Optional[str] = Field(None, description="Timestamp of status check")
    
    class Config:
        json_schema_extra = {
            "example": {
                "service_name": "httpd",
                "service_status": "UP",
                "host_name": "host1",
                "timestamp": "2024-01-29T10:30:00Z"
            }
        }


class ApplicationStatus(BaseModel):
    application_name: str = Field(..., description="Name of the application")
    application_status: str = Field(..., pattern="^(UP|DOWN)$", description="Status of the application")
    host_name: str = Field(..., description="Hostname where application runs")
    timestamp: Optional[str] = Field(None, description="Timestamp of status check")
    dependent_services: ServiceStatus = Field(None, description="List of dependent services")
    
    class Config:
        json_schema_extra = {
            "example": {
                "application_name": "rbcapp1",
                "application_status": "UP",
                "host_name": "host1",
                "timestamp": "2024-01-29T10:30:00Z"
            }
        }


class HealthCheckResponse(BaseModel):
    status: str
    services: Optional[List[ServiceStatus]] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


class StatusResponse(BaseModel):
    message: str
    data: Optional[dict] = None
