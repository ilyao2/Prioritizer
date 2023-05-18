"""Вспомогательные функции для работы с идеями"""
from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncSession

from facade import CRUD
from models import idea
from schemas import NavigationResult, Response, ResponseStatus
from .schemas import Idea, IdeaResponse


class IdeaFacade(CRUD):
    """Класс для работы с фасадом идей"""

    def __init__(self):
        super().__init__(idea)

    async def read_expand(self, idea_id: int, session: AsyncSession) -> Response:
        """Прочитать со всеми дочерними записями"""
        top_cte = idea.select().where(idea.c.id == idea_id).cte('top_idea', recursive=True)
        bottom_cte = idea.select().join(top_cte, idea.c.parent == top_cte.c.id)
        query = select(top_cte.union(bottom_cte))
        result = await session.execute(query)
        rows_list = result.all()
        if not rows_list:
            raise HTTPException(status_code=404)
        return self._create_response(ResponseStatus.SUCCESS, 'Read', rows_list)

    def _create_response(self, status: ResponseStatus, description: str = None, rows: Sequence[Row] = None,
                         navigation_result: NavigationResult | None = None) -> Response:
        return IdeaResponse(
            status=status,
            description=description,
            navigation_result=navigation_result,
            data=tuple(map(self._get_idea_response, rows))
        )

    @staticmethod
    def _get_idea_response(_idea) -> Idea:
        """Конвертирует строку БД с идей в схему данных"""
        return Idea(
            id=_idea.id,
            title=_idea.title,
            description=_idea.description,
            author=_idea.author,
            parent=_idea.parent
        )
    