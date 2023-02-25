import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from alert.settings import Settings

from alert.api.v1.alert_api import alert_api_router

settings = Settings()
api_prefix = f'/api/v{settings.api_version}'
app = FastAPI(title=settings.project_name, openapi_url=f"/openapi.json")
app.include_router(alert_api_router)

@app.on_event("startup")
async def startup_event() -> None:

    logger.info("Starting up.")
    logger.info("Alert API ready.")

@app.on_event("shutdown")
async def shutdown_event() -> None:
    """
    Shuting down
    """
    logger.info("Shuting down...")
    logger.info("Done. Bye")
    
if __name__ == "__main__":
    uvicorn.run("main:app",
                host=settings.host,
                port=settings.port,
                log_level=settings.log_level,
                reload=settings.hot_reload,
                workers=1)
