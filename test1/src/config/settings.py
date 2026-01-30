from pydantic_settings import BaseSettings
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

class Settings(BaseSettings):
    
    app_name: str = "RBC Application Monitoring API"
    app_version: str = "1.0.0"
    api_v1_prefix: str = "/api/v1"
    debug: bool = True

    host: str = "localhost"
    port: int = 9200
    elasticsearch_index: str = "service-status"

    elasticsearch_url: str = os.environ.get('ELASTICSEARCH_URL')
    elasticsearch_api_key: str = os.environ.get('ELASTICSEARCH_API_KEY')
    
    application_name: str = "rbcapp1"
    
    cors_origins: List[str] = ["*"]

    services: List[str] = ["httpd", "rabbitmq-server", "postgresql"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()