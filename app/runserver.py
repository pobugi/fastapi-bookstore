import uvicorn

from app.core.config import settings


def run_uvicorn_server():
    uvicorn.run(
        "app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True,
    )
