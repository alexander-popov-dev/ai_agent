from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.user.repository import UserRepository
from src.application.user.service import UserService
from src.core.logging.mixin import LoggedMixin


class UserProvider(Provider, LoggedMixin):

    @provide(scope=Scope.REQUEST)
    def get_repository(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def get_service(self, repository: UserRepository) -> UserService:
        return UserService(repository=repository)
