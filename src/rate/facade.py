"""Вспомогательные функции для работы с оценками"""
from typing import Sequence

from sqlalchemy import Row

from facade import CRUD
from models import metric, rate
from schemas import NavigationResult, Response, ResponseStatus
from .schemas import Rate, RateResponse


class RateFacade(CRUD):
    """Класс для работы с фасадом для оценок"""

    def __init__(self):
        super().__init__(rate)

    def _create_response(self, status: ResponseStatus, description: str = None, rows: Sequence[Row] = None,
                         navigation_result: NavigationResult | None = None) -> Response:
        return RateResponse(
            status=status,
            description=description,
            navigation_result=navigation_result,
            data=tuple(map(self._get_rate_response, rows))
        )

    @staticmethod
    def _get_rate_response(_rate: rate) -> Rate:
        """Конвертирует строку БД с оценкой в схему данных"""
        return Rate(
            id=_rate.id,
            metric=_rate.metric,
            person=_rate.person,
            value=_rate.value
        )
