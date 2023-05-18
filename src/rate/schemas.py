"""Схемы данных для работы с оценками"""

from pydantic import BaseModel, Field

from schemas import Response


class Rate(BaseModel):
    """Основная схема оценки"""
    id: int
    metric: int
    person: int
    value: int = Field(ge=0, le=100)


class RateInsert(BaseModel):
    """Схема оценки для создания"""
    metric: int
    person: int
    value: int = Field(ge=0, le=100)


class RateUpdate(BaseModel):
    """Схема оценки для изменения"""
    value: int = Field(ge=0, le=100)


class RateResponse(Response):
    """Схема ответа с оценки"""
    data: list[Rate] | None
