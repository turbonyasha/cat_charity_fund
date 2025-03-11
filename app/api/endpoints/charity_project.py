from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.api.validators import validate_unique_name
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectUpdate, CharityProjectResponse
)
from app.api.validators import (
    validate_project_exists, validate_project_is_open,
    validate_project_invested_amount
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
    session: AsyncSession = Depends(get_async_session)
):
    await validate_unique_name(project.name, session=session)
    return await charity_project_crud.create(project, session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectResponse,
    dependencies=[Depends(current_superuser)]
)
async def update_project(
    project_id: int,
    project_data: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    project = await charity_project_crud.get(project_id, session)
    await validate_project_exists(project)
    if project_data.name:
        await validate_unique_name(
            project_data.name, project_id=project_id, session=session
        )
    return await charity_project_crud.update(
        project, project_data, session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectResponse,
    dependencies=[Depends(current_superuser)]
)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    project = await charity_project_crud.get(project_id, session)
    await validate_project_exists(project)
    await validate_project_is_open(project)
    await validate_project_invested_amount(project)
    deleted_project = await charity_project_crud.remove(project, session)
    return deleted_project
