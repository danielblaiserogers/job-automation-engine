from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.core.database import init_db
from app.api.v1.endpoints.jobs import router as jobs_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables on startup
    init_db()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)
@app.get("/")
def read_root():
    return {
        "status": "online",
        "docs": "http://127.0.0.1:8000/docs",
        "jobs_endpoint": "http://127.0.0.1:8000/api/v1/jobs/"
    }
# Register endpoints under /api/v1
app.include_router(jobs_router, prefix="/api/v1")