from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models import CharityProject, Donation, User
from app.core.investment import invest_in_project
from app.schemas.charity_project import CharityProjectCreate, CharityProjectUpdate
from typing import List
from .base import CRUDBase
from fastapi import HTTPException


class CharityProjectCRUD(CRUDBase):

    async def create(self, obj_in: CharityProjectCreate, session: AsyncSession):
        # Создаем проект
        project = await super().create(obj_in, session)
        
        # После создания проекта, запускаем процесс "инвестирования"
        await invest_in_project(project, session)
        
        return project

    async def update(self, db_obj: CharityProject, obj_in: CharityProjectUpdate, session: AsyncSession) -> CharityProject:
        # Проверяем, что размер требуемой суммы не меньше уже внесенной
        if obj_in.full_amount < db_obj.invested_amount:
            raise HTTPException(status_code=400, detail="New required amount cannot be less than the invested amount")
        
        # Обновляем проект
        return await super().update(db_obj, obj_in, session)

    async def remove(self, db_obj: CharityProject, session: AsyncSession) -> CharityProject:
        # Удалять проекты можно только если в проект еще не были внесены средства
        if db_obj.invested_amount > 0:
            raise HTTPException(status_code=400, detail="Cannot delete a project with funds")
        return await super().remove(db_obj, session)

    async def get_projects(self, session: AsyncSession) -> List[CharityProject]:
        # Получаем все проекты, для отображения пользователям
        result = await session.execute(select(CharityProject).options(selectinload(CharityProject.donations)))
        return result.scalars().all()

    async def get_project(self, obj_id: int, session: AsyncSession) -> CharityProject:
        # Получаем проект по id
        return await super().get(obj_id, session)


charity_project_crud = CharityProjectCRUD(CharityProject)