from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AIProviderSchema(BaseModel):
    id: UUID
    name: str
    display_name: str
    base_url: str | None = None
    api_key: str | None = None

    model_config = ConfigDict(from_attributes=True)

    def set_api_key(self, api_key: str) -> None:
        self.api_key = api_key


class AIModelSchema(BaseModel):
    id: UUID
    name: str
    display_name: str

    model_config = ConfigDict(from_attributes=True)


class AIModelWithProviderSchema(AIModelSchema):
    provider: AIProviderSchema
