from pydantic_settings import BaseSettings
from typing import List, Dict


class Settings(BaseSettings):
    
    app_name: str = "RBC Application Monitoring API"
    app_version: str = "1.0.0"
    api_v1_prefix: str = "/api/v1"
    debug: bool = True

    api_url: str = "http://localhost:8000/v1/add"
    output_dir: str = "test1/data"
    
    elasticsearch_hosts: List[str] = ["http://localhost:9200"]
    elasticsearch_index: str = "service-status"
    
    monitored_services: List[str] = ["httpd", "rabbitmq-server", "postgresql"]
    application_name: str = "rbcapp1"
    
    cors_origins: List[str] = ["*"]

    services: List[str] = ["httpd", "rabbitmq-server", "postgresql"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()