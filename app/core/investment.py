from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from app.models import CharityProject, Donation
from datetime import datetime


async def invest_in_project(session: AsyncSession, project_id: int):
    # Получаем проект
    project = await session.execute(select(CharityProject).where(CharityProject.id == project_id))
    project = project.scalars().first()

    if not project:
        return None

    # Получаем все "свободные" пожертвования
    free_donations = await session.execute(select(Donation).filter(Donation.project == None))
    free_donations = free_donations.scalars().all()

    total_investment = sum(donation.amount for donation in free_donations)

    remaining_amount = project.full_amount - project.invested_amount
    if total_investment > remaining_amount:
        total_investment = remaining_amount

    # Добавляем средства в проект
    project.invested_amount += total_investment

    if project.invested_amount >= project.full_amount:
        project.fully_invested = True
        project.close_date = datetime.now()

    # Сохраняем изменения
    await session.commit()
    await session.refresh(project)
    return project
