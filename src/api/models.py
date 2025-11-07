from typing import Any
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Integer,
)
from sqlalchemy.orm import declarative_base

Base: Any = declarative_base()


class IncidentDB(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    status = Column(String, index=True)
    source = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
