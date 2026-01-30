from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1.endpoints import router as endpoints
from src.config.settings import Settings
from src.services.monitor_services import ServiceMonitor
from src.config.logger import logger
from fastapi.responses import JSONResponse

def create_app():

    settings: Settings = Settings()

    app = FastAPI( 
        title=settings.app_name,
        version=settings.app_version,
        description="RESTful API for monitoring RBC Application services",
        docs_url="/docs",
        redoc_url="/redoc",
        debug=settings.debug
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(endpoints)

    @app.on_event("startup")
    async def startup_monitoring():
        logger.__info__("Starting service monitoring on startup")

        monitor_services = ServiceMonitor(settings.services)
        results = monitor_services.monitor_all_services()

        for result in results:
            name = result.get('service_name') or result.get('application_name')
            status = result.get('status')
            logger.__info__(f"{name}: {status}")

    @app.get("/")
    def health_check():
        return {"status": "ok"}

    @app.exception_handler(Exception)
    async def exception_handler(request, exc):
        logger.__error__(f"Global exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

    return app

app = create_app()

