"""Схемы данных для работы с метриками"""

from pydantic import BaseModel, Field

from schemas import Response


class Metric(BaseModel):
    """Основная схема метрики"""
    id: int
    title: str
    idea: int
    type: list[str] | None = None


class MetricInsert(BaseModel):
    """Схема метрики для создания"""
    title: str = Field(min_length=1)
    idea: int | None = None
    type: list[str] | None = None


class MetricUpdate(BaseModel):
    """Схема метрики для изменения"""
    title: str | None = Field(min_length=1)
    idea: int | None = None
    type: list[str] | None = None


class MetricResponse(Response):
    """Схема ответа с метриками"""
    data: list[Metric] | None
