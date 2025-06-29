from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time
from app.logger import get_logger
from app.database import init_database, close_database
from app.api.teams.routes import router as teams_router

logger = get_logger(__name__)

app = FastAPI(
    title="Football AI Assistant API",
    description="Simple API for football data",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    logger.info(
        "Incoming request",
        method=request.method,
        url=str(request.url),
        client_ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )
    
    try:
        response = await call_next(request)
        
        process_time = time.time() - start_time
        logger.info(
            "Request completed",
            method=request.method,
            url=str(request.url),
            status_code=response.status_code,
            process_time=round(process_time, 3)
        )
        
        return response
        
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            "Request failed",
            method=request.method,
            url=str(request.url),
            error=str(e),
            process_time=round(process_time, 3)
        )
        raise


@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    
    return {
        "message": "Football AI Assistant API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/status")
async def status():
    logger.info("Status endpoint accessed")
    
    return {
        "success": True,
        "message": "API works correctly",
        "version": "1.0.0",
        "timestamp": time.time()
    }


app.include_router(teams_router)


@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up")
    await init_database()


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down")
    await close_database()


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Football AI Assistant API")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 