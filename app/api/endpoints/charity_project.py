from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from app.schemas.charity_project import CharityProjectCreate, CharityProjectUpdate, CharityProjectResponse
from app.crud.charity_project import CharityProjectCRUD
from typing import List

router = APIRouter()
charity_project_crud = CharityProjectCRUD()

# Получение всех проектов
@router.get("/charity_project", response_model=List[CharityProjectResponse])
async def list_projects(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)):
    projects = await charity_project_crud.get_multi(db)
    return projects

# Создание нового проекта
@router.post("/charity_project", response_model=CharityProjectResponse)
async def create_project(project_data: CharityProjectCreate, db: AsyncSession = Depends(get_async_session)):
    project = await charity_project_crud.create(project_data, db)
    return project

# Обновление данных проекта
@router.patch("/charity_project/{project_id}", response_model=CharityProjectResponse)
async def update_project(project_id: int, project_data: CharityProjectUpdate, db: AsyncSession = Depends(get_async_session)):
    db_obj = await charity_project_crud.get(project_id, db)
    if db_obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    updated_project = await charity_project_crud.update(db_obj, project_data, db)
    return updated_project

# Удаление проекта
@router.delete("/charity_project/{project_id}", response_model=CharityProjectResponse)
async def delete_project(project_id: int, db: AsyncSession = Depends(get_async_session)):
    db_obj = await charity_project_crud.get(project_id, db)
    if db_obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    deleted_project = await charity_project_crud.remove(db_obj, db)
    if deleted_project is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete project with investments")
    return deleted_project
