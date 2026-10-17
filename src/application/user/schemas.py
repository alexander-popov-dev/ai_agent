from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.application.niche.schemas import NicheScheme


class UserSchema(BaseModel):
    id: UUID
    external_id: str
    name: str
    niches: list[NicheScheme] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
