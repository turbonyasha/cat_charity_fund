from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import CharityProject


NOT_FOUND_TEXT = 'Проект не найден.'
CANT_DELETE_INVESTMENTED_PROJECT = (
    'Нельзя удалить проект, в который уже поступили средства!')
CANT_DELETE_CLOSED_PROJECT = (
    'Нельзя удалить закрытый проект!')
PROJECT_NAME_ALREADY_EXISTS = 'Проект с таким именем уже существует!'
DONATION_POSITIVE = 'Сумма пожертвования должна быть больше 0.'


async def validate_unique_name(
    name: str,
    project_id: Optional[int] = None,
    session: AsyncSession = None
):
    result = await session.execute(select(CharityProject).filter(
        CharityProject.name == name
    ))
    existing_project = result.scalar_one_or_none()
    if existing_project and (
            project_id is None or existing_project.id != project_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PROJECT_NAME_ALREADY_EXISTS
        )


def validate_donation_amount(donation_amount: float):
    if donation_amount <= 0:
        raise HTTPException(status_code=422, detail=DONATION_POSITIVE)


def validate_project_exists(project):
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=NOT_FOUND_TEXT
        )


def validate_project_is_open(project):
    if project.close_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=CANT_DELETE_CLOSED_PROJECT
        )


def validate_project_invested_amount(project):
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=CANT_DELETE_INVESTMENTED_PROJECT
        )
