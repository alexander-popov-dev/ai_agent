from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    id: UUID
    external_id: str
    name: str

    model_config = ConfigDict(from_attributes=True)
