from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, field_serializer, ConfigDict

from src.schemas.Shared.Domain import Domain
from src.schemas.Shared.Environment import Environment


class GetUsersResponse(BaseModel):
    id: UUID
    created_at: datetime
    login: str
    project_id: UUID
    env: Environment
    domain: Domain
    locktime: datetime | None
