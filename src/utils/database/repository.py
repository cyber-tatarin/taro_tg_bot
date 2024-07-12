from abc import ABC, abstractmethod
from typing import Any, TypeVar

from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.database.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class AbstractRepository(ABC):
    @abstractmethod
    async def add(self, data):
        raise NotImplementedError

    @abstractmethod
    async def find_one_or_none(self):
        raise NotImplementedError
    
    @abstractmethod
    async def find_all(self):
        raise NotImplementedError
    
    @abstractmethod
    async def update(self):
        raise NotImplementedError

    @abstractmethod
    async def delete(self):
        raise NotImplementedError
    

class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    def _prepare_object(self, obj_in: CreateSchemaType | dict[str, Any]) -> dict:
        if isinstance(obj_in, dict):
            return obj_in
        else:
            return obj_in.model_dump(exclude_unset=True)
    
    async def add(
        self, obj_in: CreateSchemaType | dict[str, Any]
    ) -> ModelType | None:
        create_data = self._prepare_object(obj_in)
        # try:
        stmt = insert(self.model).values(**create_data).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().first()
        # except (SQLAlchemyError, Exception) as e:
        #     if isinstance(e, SQLAlchemyError):
        #         msg = "Database Exc: Cannot insert data into table"
        #         print(e)
        #     elif isinstance(e, Exception):
        #         msg = "Unknown Exc: Cannot insert data into table"
        #         print(e)

            # logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
        # print(msg)

    async def find_one_or_none(self, *filter, **filter_by) -> ModelType | None:
        stmt = select(self.model).filter(*filter).filter_by(**filter_by)
        return await self.session.scalar(stmt)
    
    async def find_all(
        self,
        *filter,
        offset: int = 0,
        limit: int = 100,
        **filter_by
    ) -> list[ModelType]:
        stmt = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(
        cls,
        *where,
        obj_in: UpdateSchemaType | dict[str, Any]
    ) -> ModelType | None:
        update_data = cls._prepare_object(obj_in)
        stmt = (
            update(cls.model)
            .where(*where)
            .values(**update_data)
            .returning(cls.model)
        )
        result = await cls.session.execute(stmt)
        return result.scalars().all()

    async def delete(cls, *filter, **filter_by) -> None:
        stmt = delete(cls.model).filter(*filter).filter_by(**filter_by)
        await cls.session.execute(stmt)
