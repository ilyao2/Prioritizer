"""Схемы данных для работы со вспомогательными методами"""

from pydantic import BaseModel, Field


class BriceSchema(BaseModel):
    """Схема для расчета по BRISE"""
    business: float = Field(ge=0, le=1)
    reach: int = Field(ge=0)
    impact: float = Field(ge=0, le=3)
    confidence: float = Field(ge=0, le=1)
    effort: int = Field(ge=0)
