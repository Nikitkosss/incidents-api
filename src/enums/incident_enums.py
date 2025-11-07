from enum import Enum


class IncidentStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    closed = "closed"
    reopened = "reopened"


class IncidentSource(str, Enum):
    operator = "operator"
    monitoring = "monitoring"
    partner = "partner"
