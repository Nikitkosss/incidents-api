import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    POSTGRES_SERVER: str = os.environ.get("POSTGRES_SERVER")
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB")
    POSTGRES_PORT: int = os.environ.get("POSTGRES_PORT")


settings = Settings()
