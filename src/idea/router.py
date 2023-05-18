"""Роутер для идей"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from consts import SOMETHING_WRONG
from database import get_async_session
from schemas import PageNavigation
from .facade import IdeaFacade
from .schemas import IdeaInsert, IdeaResponse, IdeaUpdate

router = APIRouter(
    prefix='/idea',
    tags=['Idea']
)
facade = IdeaFacade()


@router.post('/')
async def create_idea(idea_data: IdeaInsert, session: AsyncSession = Depends(get_async_session)) -> IdeaResponse:
    """Создание идеи"""
    response = await facade.create(idea_data, session)
    if not isinstance(response, IdeaResponse):
        raise HTTPException(500, SOMETHING_WRONG)
    return response


@router.get('/{idea_id}')
async def read_idea(idea_id: int, session: AsyncSession = Depends(get_async_session)) -> IdeaResponse:
    """Чтение идеи"""
    response = await facade.read(idea_id, session)
    if not isinstance(response, IdeaResponse):
        raise HTTPException(500, SOMETHING_WRONG)
    return response


@router.get('/{idea_id}/expand')
async def read_expanded_idea(idea_id: int, session: AsyncSession = Depends(get_async_session)) -> IdeaResponse:
    """Чтение идеи со всеми дочерними идеями"""
    response = await facade.read_expand(idea_id, session)
    if not isinstance(response, IdeaResponse):
        raise HTTPException(500, SOMETHING_WRONG)
    return response


@router.post('/list')
async def read_ideas_list(navigation: PageNavigation,
                          session: AsyncSession = Depends(get_async_session)) -> IdeaResponse:
    """Чтение списка идей"""
    response = await facade.read_list(navigation, session)
    if not isinstance(response, IdeaResponse):
        raise HTTPException(500, SOMETHING_WRONG)
    return response


@router.put('/{idea_id}')
async def update_idea(idea_id: int, idea_data: IdeaUpdate,
                      session: AsyncSession = Depends(get_async_session)) -> IdeaResponse:
    """Изменение идеи"""
    response = await facade.update(idea_id, idea_data, session)
    if not isinstance(response, IdeaResponse):
        raise HTTPException(500, SOMETHING_WRONG)
    return response


@router.delete('/{idea_id}')
async def delete_ideas(idea_id: int, session: AsyncSession = Depends(get_async_session)) -> IdeaResponse:
    """Удаление идеи"""
    response = await facade.delete(idea_id, session)
    if not isinstance(response, IdeaResponse):
        raise HTTPException(500, SOMETHING_WRONG)
    return response


@router.delete('/')
async def delete_ideas(ideas: set[int], session: AsyncSession = Depends(get_async_session)) -> IdeaResponse:
    """Удаление идеи"""
    response = await facade.delete_list(ideas, session)
    if not isinstance(response, IdeaResponse):
        raise HTTPException(500, SOMETHING_WRONG)
    return response
