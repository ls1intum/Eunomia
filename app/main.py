import logging
from fastapi import FastAPI

from app.routers.mail_router import router as mail_router
from app.common.logging_config import setup_logging
from app.managers.thread_manager import ThreadManager

app = FastAPI()
thread_manager = ThreadManager()

setup_logging()

@app.on_event("startup")
async def startup_event():
    logging.info("FastAPI application startup...")

@app.on_event("shutdown")
def shutdown_event():
    """
    Gracefully stop all threads on shutdown.
    """
    logging.info("FastAPI application shutting down...")
    thread_manager.stop_all()

# Include the router that handles mail endpoints
app.include_router(mail_router, prefix="/mail", tags=["mail"])