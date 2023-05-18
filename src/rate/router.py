"""Роутер для метрик"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from consts import SOMETHING_WRONG
from database import get_async_session
from schemas import PageNavigation
from .facade import RateFacade
from .schemas import RateInsert, RateResponse, RateUpdate

router = APIRouter(
    prefix='/rate',
    tags=['Rate']
)
facade = RateFacade()


@router.post('/')
async def create_rate(rate_data: RateInsert, session: AsyncSession = Depends(get_async_session)) -> RateResponse:
    """Создание оценки"""
    response = await facade.create(rate_data, session)
    if not isinstance(response, RateResponse):
        raise HTTPException(500, SOMETHING_WRONG)
    return response


@router.get('/{rate_id}')
async def read_rate(rate_id: int, session: AsyncSession = Depends(get_async_session)) -> RateResponse:
    """Чтение оценки"""
    response = await facade.read(rate_id, session)
    if not isinstance(response, RateResponse):
        raise HTTPException(500, SOMETHING_WRONG)
    return response


@router.post('/list')
async def read_metrics_list(navigation: PageNavigation,
                            session: AsyncSession = Depends(get_async_session)) -> RateResponse:
    """Чтение списка оценок"""
    response = await facade.read_list(navigation, session)
    if not isinstance(response, RateResponse):
        raise HTTPException(500, SOMETHING_WRONG)
    return response


@router.put('/{rate_id}')
async def update_rate(rate_id: int, rate_data: RateUpdate,
                        session: AsyncSession = Depends(get_async_session)) -> RateResponse:
    """Изменение оценки"""
    response = await facade.update(rate_id, rate_data, session)
    if not isinstance(response, RateResponse):
        raise HTTPException(500, SOMETHING_WRONG)
    return response


@router.delete('/{rate_id}')
async def delete_rate(rate_id: int, session: AsyncSession = Depends(get_async_session)) -> RateResponse:
    """Удаление оценки"""
    response = await facade.delete(rate_id, session)
    if not isinstance(response, RateResponse):
        raise HTTPException(500, SOMETHING_WRONG)
    return response


@router.delete('/')
async def delete_rates_list(rates: set[int], session: AsyncSession = Depends(get_async_session)) -> RateResponse:
    """Удаление нескольких оценок"""
    response = await facade.delete_list(rates, session)
    if not isinstance(response, RateResponse):
        raise HTTPException(500, SOMETHING_WRONG)
    return response
