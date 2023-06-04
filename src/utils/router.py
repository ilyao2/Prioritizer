"""Роутер для вспомогательных методов"""

from fastapi import APIRouter

from .schemas import BriceSchema

router = APIRouter(
    prefix='/utils',
    tags=['Utils']
)


@router.post('/')
async def create_rate(brice_obj: BriceSchema) -> float:
    """Создание оценки"""
    result = (brice_obj.business * brice_obj.reach * brice_obj.impact * brice_obj.confidence) / brice_obj.effort
    return result
