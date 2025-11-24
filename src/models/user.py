import uuid
from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy import String, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID as ORM_UUID

from src.models.base import Base
from src.schemas.Shared.Domain import Domain
from src.schemas.Shared.Environment import Environment


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(ORM_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,
                                                 default=lambda: datetime.now(timezone.utc))
    login: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    project_id: Mapped[UUID] = mapped_column(ORM_UUID(as_uuid=True), nullable=False, index=True)
    env: Mapped[Environment] = mapped_column(Enum(Environment, name='environment_enum'), nullable=False)
    domain: Mapped[Domain] = mapped_column(Enum(Domain, name='domain_enum'), nullable=False)
    locktime: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
