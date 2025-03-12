from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models import CharityProject
from .base import CRUDBase


class CharityProjectCRUD(CRUDBase):
    async def get_projects(
        self,
        session: AsyncSession
    ) -> list[CharityProject]:
        result = await session.execute(
            select(CharityProject).options(
                selectinload(CharityProject.donations)))
        return result.scalars().all()


charity_project_crud = CharityProjectCRUD(CharityProject)
