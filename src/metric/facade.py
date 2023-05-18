"""Вспомогательные функции для работы с метриками"""
from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import any_, Row, select
from sqlalchemy.ext.asyncio import AsyncSession

from facade import CRUD
from models import idea, metric
from schemas import NavigationResult, Response, ResponseStatus
from .schemas import Metric, MetricResponse


class MetricFacade(CRUD):
    """Класс для работы с фасадом для метрик"""

    def __init__(self):
        super().__init__(metric)

    async def read_by_idea(self, idea_id: int, session: AsyncSession) -> Response:
        """Читаем все метрики для идеи"""
        top_cte = select(idea.c.id, idea.c.parent).where(idea.c.id == idea_id).cte('ideas', recursive=True)
        bottom_cte = select(idea.c.id, idea.c.parent).join(top_cte, idea.c.id == top_cte.c.parent)
        ideas_cte = select(top_cte.union(bottom_cte).c.id)
        query = metric.select().where(metric.c.idea == any_(select(ideas_cte.c.id)))
        result = await session.execute(query)
        rows_list = result.all()
        return self._create_response(ResponseStatus.SUCCESS, 'Read', rows_list)

    def _create_response(self, status: ResponseStatus, description: str = None, rows: Sequence[Row] = None,
                         navigation_result: NavigationResult | None = None) -> Response:
        return MetricResponse(
            status=status,
            description=description,
            navigation_result=navigation_result,
            data=tuple(map(self._get_metric_response, rows))
        )

    @staticmethod
    def _get_metric_response(_metric: metric) -> Metric:
        """Конвертирует строку БД с метрикой в схему данных"""
        return Metric(
            id=_metric.id,
            title=_metric.title,
            idea=_metric.idea,
            type=_metric.type
        )
