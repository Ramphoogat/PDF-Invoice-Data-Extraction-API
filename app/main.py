from fastapi import FastAPI
from app.api.endpoints import extraction
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(extraction.router, prefix=settings.API_V1_STR, tags=["extraction"])

@app.on_event("startup")
def startup_db():
    from app.db.session import engine, Base
    Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "PDF Data Extraction API is running"}
