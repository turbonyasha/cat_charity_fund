from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import CharityProject
from app.core.investment import invest_in_project
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectUpdate
)
from app.api.validators import (
    PROJECT_NAME_ALREADY_EXISTS, CANT_DELETE_INVESTMENTED_PROJECT
)

from .base import CRUDBase


FULL_INVESTED = 'Нельзя обновить полностью проинвестированный проект'
NEW_FULL_AMOUNT_CANT_BE_LESS = (
    'Новая сумма сбора не может быть меньше предыдущей.'
)


class CharityProjectCRUD(CRUDBase):
    async def create(
            self,
            project: CharityProjectCreate,
            session: AsyncSession
    ):
        existing_project = await session.execute(
            select(CharityProject).filter(CharityProject.name == project.name)
        )
        existing_project = existing_project.scalars().first()
        if existing_project:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=PROJECT_NAME_ALREADY_EXISTS
            )
        project = await super().create(project, session)
        await invest_in_project(project, session)
        return project

    async def update(
        self,
        project: CharityProject,
        new_project_data: CharityProjectUpdate,
        session: AsyncSession
    ) -> CharityProject:
        if project.fully_invested:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=FULL_INVESTED)
        if new_project_data.full_amount is not None:
            if new_project_data.full_amount < project.invested_amount:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=NEW_FULL_AMOUNT_CANT_BE_LESS)
        if new_project_data.full_amount is not None:
            project.full_amount = new_project_data.full_amount
        if new_project_data.description is not None:
            project.description = new_project_data.description
        return await super().update(project, new_project_data, session)

    async def remove(
        self,
        project: CharityProject,
        session: AsyncSession
    ) -> CharityProject:
        if project.invested_amount > 0:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=CANT_DELETE_INVESTMENTED_PROJECT)
        return await super().remove(project, session)

    async def get_projects(
        self,
        session: AsyncSession
    ) -> list[CharityProject]:
        result = await session.execute(
            select(CharityProject).options(
                selectinload(CharityProject.donations)))
        return result.scalars().all()

    async def get_project(
        self,
        project: int,
        session: AsyncSession
    ) -> CharityProject:
        return await super().get(project, session)


charity_project_crud = CharityProjectCRUD(CharityProject)
