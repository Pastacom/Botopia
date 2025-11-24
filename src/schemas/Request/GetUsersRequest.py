from uuid import UUID
from pydantic import BaseModel

from src.schemas.Shared.Domain import Domain
from src.schemas.Shared.Environment import Environment


class GetUsersRequest(BaseModel):
    id: UUID | None = None
    login: str | None = None
    project_id: UUID | None = None
    env: Environment | None = None
    domain: Domain | None = None
    only_available: bool = False
