from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import IncidentDB
from src.api.schemas.incident_schemas import (
    IncidentCreateRequest,
    IncidentUpdateRequest,
)
from src.api.services.base_qurey import BaseQuery
from src.enums.incident_enums import IncidentStatus
from src.setup_logger import logger


class IncidentService(BaseQuery):
    def __init__(self, session: AsyncSession):
        super().__init__(session, IncidentDB)

    @logger
    async def create_incident(self, data: IncidentCreateRequest):
        db_incident = data.model_dump(exclude_unset=True, exclude_none=True)
        db_incident["status"] = IncidentStatus.open.value
        return await self.create_object(**db_incident)

    @logger
    async def get_incidents(self, data: Optional[IncidentStatus] = None):

        result = await self.get_object_by_kwargs(status=data.value if data else None)
        return result.scalars().all()

    @logger
    async def update_incident_status(
        self, incident_id: int, data: IncidentUpdateRequest
    ):

        existing_incident_result = await self.get_object_by_kwargs(id=incident_id)
        existing_incident = existing_incident_result.scalars().first()

        if not existing_incident:
            raise HTTPException(status_code=404, detail="Инцидент не найден")

        if data.status == IncidentStatus.open:
            raise HTTPException(
                status_code=400,
                detail="Статус не может быть изменен на open.",
            )

        result = await self.update_object_by_kwargs(
            update_data={"status": data.status.value}, id=incident_id
        )

        updated_incident = result.scalars().first()

        if not updated_incident:
            raise HTTPException(status_code=500, detail="Ошибка обновления инцидента")

        return updated_incident
