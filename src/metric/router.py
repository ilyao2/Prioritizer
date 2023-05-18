"""Роутер для метрик"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from consts import SOMETHING_WRONG
from database import get_async_session
from schemas import PageNavigation
from .facade import MetricFacade
from .schemas import MetricInsert, MetricResponse, MetricUpdate

router = APIRouter(
    prefix='/metric',
    tags=['Metric']
)
facade = MetricFacade()


@router.post('/')
async def create_metric(metric_data: MetricInsert,
                        session: AsyncSession = Depends(get_async_session)) -> MetricResponse:
    """Создание метрики"""
    response = await facade.create(metric_data, session)
    if not isinstance(response, MetricResponse):
        raise HTTPException(500, SOMETHING_WRONG)
    return response


@router.get('/{metric_id}')
async def read_metric(metric_id: int, session: AsyncSession = Depends(get_async_session)) -> MetricResponse:
    """Чтение метрики"""
    response = await facade.read(metric_id, session)
    if not isinstance(response, MetricResponse):
        raise HTTPException(500, SOMETHING_WRONG)
    return response


@router.post('/by_idea')
async def read_by_idea(idea_id: int, session: AsyncSession = Depends(get_async_session)) -> MetricResponse:
    """Чтение метрик по идее"""
    response = await facade.read_by_idea(idea_id, session)
    if not isinstance(response, MetricResponse):
        raise HTTPException(500, SOMETHING_WRONG)
    return response


@router.post('/list')
async def read_metrics_list(navigation: PageNavigation,
                            session: AsyncSession = Depends(get_async_session)) -> MetricResponse:
    """Чтение списка метрик"""
    response = await facade.read_list(navigation, session)
    if not isinstance(response, MetricResponse):
        raise HTTPException(500, SOMETHING_WRONG)
    return response


@router.put('/{metric_id}')
async def update_metric(metric_id: int, metric_data: MetricUpdate,
                        session: AsyncSession = Depends(get_async_session)) -> MetricResponse:
    """Изменение метрики"""
    response = await facade.update(metric_id, metric_data, session)
    if not isinstance(response, MetricResponse):
        raise HTTPException(500, SOMETHING_WRONG)
    return response


@router.delete('/{metric_id}')
async def delete_metric(metric_id: int, session: AsyncSession = Depends(get_async_session)) -> MetricResponse:
    """Удаление метрики"""
    response = await facade.delete(metric_id, session)
    if not isinstance(response, MetricResponse):
        raise HTTPException(500, SOMETHING_WRONG)
    return response


@router.delete('/')
async def delete_metrics_list(metrics: set[int], session: AsyncSession = Depends(get_async_session)) -> MetricResponse:
    """Удаление нескольких метрик"""
    response = await facade.delete_list(metrics, session)
    if not isinstance(response, MetricResponse):
        raise HTTPException(500, SOMETHING_WRONG)
    return response
