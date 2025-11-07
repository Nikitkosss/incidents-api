import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from src.database import create_tables_sync
from src.setup_logger import setup_logger

from src.api.routers import incident_routers
from src.middleware import (
    CatchExceptionsMiddleware,
)


os.environ["TZ"] = "Europe/Moscow"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    await setup_logger()
    create_tables_sync()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def custom_openapi() -> dict:
    openapi_schema = get_openapi(
        title="Маленький API-сервис для учёта инцидентов.",
        version="1.0.0",
        description="Кейс-задание",
        routes=app.routes,
    )

    return openapi_schema


app.openapi = custom_openapi


app.add_middleware(CatchExceptionsMiddleware)


app.include_router(incident_routers.router)
