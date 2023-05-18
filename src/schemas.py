"""Общие схемы данных"""
from enum import StrEnum

from pydantic import BaseModel, Field


class ResponseStatus(StrEnum):
    """Перечисление статусов выполнения запросов"""
    SUCCESS: str = 'Success'
    FAILED: str = 'Failed'
    WARNING: str = 'Warning'


class PageNavigation(BaseModel):
    """Модель навигации"""
    objects: list[int] | None = None
    limit: int = Field(gt=0)
    page: int = Field(ge=0)


class NavigationResult(BaseModel):
    more: bool
    data: BaseModel | None = None


class Response(BaseModel):
    """Основная схема ответов"""
    status: ResponseStatus
    description: str | None
    navigation_result: NavigationResult | None = None
