from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import CharityProject
from typing import Optional

async def validate_unique_name(name: str, project_id: Optional[int] = None, session: AsyncSession = None):
    # Проверяем, существует ли проект с таким же именем
    result = await session.execute(select(CharityProject).filter(CharityProject.name == name))
    existing_project = result.scalar_one_or_none()

    # Если проект найден и его ID не совпадает с переданным (для случая обновления)
    if existing_project and (project_id is None or existing_project.id != project_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A project with this name already exists.")
