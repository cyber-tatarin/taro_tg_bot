from abc import ABC, abstractmethod
from typing import Type

from src.repositories.moon_data_repository import MoonDataRepository
from src.repositories.recommendation_repository import RecommendationRepository
from src.repositories.user_repository import UserRepository
from src.utils.database.database import async_session_maker

UserRepository
class InitUoW(ABC):
    users: Type[UserRepository]
    recommendations: Type[RecommendationRepository]
    moon_data: Type[MoonDataRepository]

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError()

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError()

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError()


class UoW(InitUoW):
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UserRepository(self.session)
        self.recommendations = RecommendationRepository(self.session)
        self.moon_data = MoonDataRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
