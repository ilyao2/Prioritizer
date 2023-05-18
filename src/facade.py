"""Общие вспомогательные методы"""
from abc import ABC, abstractmethod
from typing import Sequence

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import Row, Table
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import NavigationResult, PageNavigation, Response, ResponseStatus


class CRUD(ABC):
    """Класс описывающий CRUD фасад"""
    def __init__(self, model: Table):
        self._model = model

    async def create(self, create_data: BaseModel, session: AsyncSession) -> Response:
        """Создание"""
        stmt = self._model.insert().values(**create_data.dict()).returning(self._model)
        result = await session.execute(stmt)
        await session.commit()
        row = result.one_or_none()
        if row is None:
            result = self._create_response(ResponseStatus.FAILED, 'Failed', None)
        else:
            result = self._create_response(ResponseStatus.SUCCESS, 'Created', [row])
        return result

    async def read(self, object_id: int, session: AsyncSession) -> Response:
        """Чтение"""
        query = self._model.select().where(self._model.c.id == object_id)
        result = await session.execute(query)
        row = result.one_or_none()
        if row is None:
            raise HTTPException(status_code=404)
        return self._create_response(ResponseStatus.SUCCESS, 'Read', [row])

    async def read_list(self, navigation: PageNavigation, session: AsyncSession) -> Response:
        """Чтение нескольких объектов"""
        query = self._model.select()
        if navigation.objects:
            query = query.where(self._model.c.id.in_(navigation.objects))
        query = query.order_by(self._model.c.id) \
            .limit(navigation.limit) \
            .offset(navigation.page*navigation.limit)
        result = await session.execute(query)
        rows_list = result.all()
        result = self._create_response(ResponseStatus.SUCCESS, 'Read', rows_list,
                                       NavigationResult(more=bool(rows_list)))
        return result

    async def update(self, object_id: int, new_data: BaseModel, session: AsyncSession) -> Response:
        """Изменение"""
        stmt = self._model.update() \
            .where(self._model.c.id == object_id) \
            .values(**new_data.dict(exclude_unset=True)) \
            .returning(self._model)
        result = await session.execute(stmt)
        await session.commit()
        row = result.one_or_none()
        if row is None:
            raise HTTPException(status_code=404)
        return self._create_response(ResponseStatus.SUCCESS, 'Updated', [row])

    async def delete(self, object_id: int, session: AsyncSession) -> Response:
        """Удаление"""
        stmt = self._model.delete().where(self._model.c.id == object_id).returning(self._model)
        result = await session.execute(stmt)
        await session.commit()
        row = result.one_or_none()
        if row is None:
            raise HTTPException(status_code=404)
        return self._create_response(ResponseStatus.SUCCESS, 'Deleted', [row])

    async def delete_list(self, objects: set[int], session: AsyncSession) -> Response:
        """Удаление нескольких"""
        stmt = self._model.delete().where(self._model.c.id.in_(objects)).returning(self._model)
        result = await session.execute(stmt)
        await session.commit()
        rows_list = result.all()
        if len(objects) == len(rows_list):
            result = self._create_response(ResponseStatus.SUCCESS, 'Deleted', rows_list)
        else:
            result = self._create_response(ResponseStatus.WARNING, f'Deleted {len(rows_list)}/{len(objects)}',
                                           rows_list)
        return result

    @abstractmethod
    def _create_response(self,
                         status: ResponseStatus,
                         description: str = None,
                         rows: Sequence[Row] = None,
                         navigation_result: NavigationResult | None = None) -> Response:
        """Метод по строке БД формирует ответ"""
