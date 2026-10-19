from src.application.user.repository import UserRepository
from src.application.user.schemas import UserSchema


class UserService:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def get_by_external_id(self, external_id: str) -> UserSchema:
        result = await self._repository.get_by_external_id(external_id=external_id)
        return UserSchema.model_validate(result)
