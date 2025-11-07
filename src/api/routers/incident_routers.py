from typing import Optional

from fastapi import APIRouter, Depends

from src.api.schemas.incident_schemas import (
    IncidentCreateRequest,
    IncidentResponse,
    IncidentUpdateRequest,
)
from src.api.services.uow import UnitOfWork, get_uow
from src.enums.incident_enums import IncidentStatus

router = APIRouter(prefix="/api/v1/incidents", tags=["Инциденты"])


@router.post("/create_incident", response_model=IncidentResponse, status_code=201)
async def create_incident(
    data: IncidentCreateRequest, uow: UnitOfWork = Depends(get_uow)
):
    return await uow.incident.create_incident(data=data)


@router.get("/get_incidents", response_model=list[IncidentResponse])
async def get_incidents(
    status: Optional[IncidentStatus] = None, uow: UnitOfWork = Depends(get_uow)
):
    return await uow.incident.get_incidents(data=status)


@router.patch("/update_incident", response_model=IncidentResponse)
async def update_incident_status(
    incident_id: int,
    data: IncidentUpdateRequest,
    uow: UnitOfWork = Depends(get_uow),
):
    return await uow.incident.update_incident_status(incident_id=incident_id, data=data)
