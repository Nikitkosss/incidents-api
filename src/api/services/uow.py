from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

from src.api.services.incident_service import IncidentService
from src.database import SessionLocal


class UnitOfWork:
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory
        self.session: AsyncSession | None = None
        self.incident: IncidentService

    async def __aenter__(self):
        self.session = self.session_factory()
        self.incident = IncidentService(self.session)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


async def get_uow() -> AsyncGenerator[UnitOfWork, None]:
    async with UnitOfWork(SessionLocal) as uow:
        yield uow
