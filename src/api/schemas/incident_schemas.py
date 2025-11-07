from datetime import datetime

from src.api.schemas.extended_base_model import ExtendedBaseModel
from src.enums.incident_enums import IncidentSource, IncidentStatus


class IncidentCreateRequest(ExtendedBaseModel):
    description: str
    source: IncidentSource


class IncidentResponse(ExtendedBaseModel):
    id: int
    description: str
    status: IncidentStatus
    source: IncidentSource
    created_at: datetime


class IncidentUpdateRequest(ExtendedBaseModel):
    status: IncidentStatus
