from uuid import UUID
from pydantic import BaseModel

from src.schemas.Shared.Domain import Domain
from src.schemas.Shared.Environment import Environment


class CreateUsersRequest(BaseModel):
    login: str
    password: str
    project_id: UUID
    env: Environment
    domain: Domain
