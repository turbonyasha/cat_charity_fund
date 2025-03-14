from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.api.validators import (
    validate_unique_name, validate_project_exists,
    validate_project_is_open, validate_project_invested_amount
)
from app.models import Donation
from app.services.investment import invest
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectUpdate,
    CharityProjectResponse
)

FULL_INVESTED = 'Нельзя обновить полностью проинвестированный проект'
NEW_FULL_AMOUNT_CANT_BE_LESS = (
    'Новая сумма сбора не может быть меньше предыдущей.'
)

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectResponse]
)
async def list_projects(
    session: AsyncSession = Depends(get_async_session)
):
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectResponse,
    dependencies=[Depends(current_superuser)]
)
async def create_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await validate_unique_name(project.name, session=session)
    new_project = await charity_project_crud.create(
        project,
        session,
        commit=False
    )
    sources = await charity_project_crud.get_non_invested_sources(
        session, model=Donation
    )
    session.add_all(invest(new_project, sources))
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectResponse,
    dependencies=[Depends(current_superuser)]
)
async def update_project(
    project_id: int,
    project_data: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
    commit_after_all_changes: bool = True
):
    project = await charity_project_crud.get(project_id, session)
    validate_project_exists(project)
    if project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=FULL_INVESTED
        )
    if project_data.name:
        await validate_unique_name(
            project_data.name, project_id=project_id, session=session
        )
    if project_data.full_amount is not None:
        if project_data.full_amount < project.invested_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=NEW_FULL_AMOUNT_CANT_BE_LESS
            )
        project.full_amount = project_data.full_amount
    if project_data.description is not None:
        project.description = project_data.description
    updated_project = await charity_project_crud.update(
        project,
        project_data,
        session,
    )
    if commit_after_all_changes:
        await session.commit()
        await session.refresh(updated_project)
    return updated_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectResponse,
    dependencies=[Depends(current_superuser)]
)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
    commit_after_all_changes: bool = True
):
    project = await charity_project_crud.get(project_id, session)
    validate_project_exists(project)
    validate_project_is_open(project)
    validate_project_invested_amount(project)
    deleted_project = await charity_project_crud.remove(project, session)
    if commit_after_all_changes:
        await session.commit()
    return deleted_project
