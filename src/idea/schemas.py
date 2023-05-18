"""Схемы данных для работы с идеями"""

from pydantic import BaseModel, Field

from schemas import Response


class Idea(BaseModel):
    """Основная схема идеи"""
    id: int
    title: str
    description: str | None = None
    author: int | None = None
    parent: int | None = None


class IdeaInsert(BaseModel):
    """Схема идеи для создания"""
    title: str = Field(min_length=1)
    description: str | None = None
    author: int | None = None
    parent: int | None = None


class IdeaUpdate(BaseModel):
    """Схема идеи для изменения"""
    title: str | None = Field(min_length=1)
    description: str | None = None
    author: int | None = None
    parent: int | None = None


class IdeaResponse(Response):
    """Схема ответа с идеями"""
    data: list[Idea] | None
