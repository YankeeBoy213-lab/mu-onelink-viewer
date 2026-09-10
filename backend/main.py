from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from app.api import devices, credentials, events, transactions, files, audit
from app.core.config import settings
from app.core.database import engine, Base
from app.core.websocket_manager import manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 MU OneLink Viewer API Starting...")
    yield
    logger.info("🛑 MU OneLink Viewer API Shutting Down...")
    await manager.disconnect_all()

app = FastAPI(
    title="MU OneLink Viewer API",
    description="Asset Device Management, Custody, Financial Access & Audit System",
    version="0.4.2-alpha",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
app.include_router(devices.router, prefix="/api/v1/devices", tags=["Devices"])
app.include_router(credentials.router, prefix="/api/v1/credentials", tags=["Credentials"])
app.include_router(events.router, prefix="/api/v1/events", tags=["Events"])
app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["Transactions"])
app.include_router(files.router, prefix="/api/v1/files", tags=["Files"])
app.include_router(audit.router, prefix="/api/v1/audit", tags=["Audit"])

@app.get("/")
async def root():
    return {
        "message": "MU OneLink Viewer API",
        "version": "0.4.2-alpha",
        "docs": "/docs",
        "status": "online"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "0.4.2-alpha"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
