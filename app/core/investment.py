from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import CharityProject, Donation


async def invest_in_project(project: CharityProject, session: AsyncSession):
    donations = await session.execute(select(Donation).filter(
        Donation.fully_invested.is_(False)))
    donations = donations.scalars().all()
    total_invested = 0
    for donation in donations:
        if total_invested < project.full_amount:
            remaining_amount = project.full_amount - total_invested
            invest_amount = min(
                donation.full_amount - donation.invested_amount,
                remaining_amount
            )
            donation.invested_amount += invest_amount
            total_invested += invest_amount
            donation.fully_invested = (
                donation.invested_amount == donation.full_amount
            )
            if donation.fully_invested:
                donation.close_date = datetime.now()
            if total_invested >= project.full_amount:
                project.fully_invested = True
                project.close_date = datetime.now()
            session.add(donation)
    if total_invested > 0:
        project.invested_amount = total_invested
        if project.invested_amount >= project.full_amount:
            project.fully_invested = True
            project.close_date = datetime.now()
    session.add(project)
    await session.commit()
    await session.refresh(project)


async def invest_donation(donation: Donation, session: AsyncSession):
    projects = await session.execute(select(CharityProject).filter(
        CharityProject.fully_invested.is_(False)))
    projects = projects.scalars().all()
    total_invested = 0
    for project in projects:
        if total_invested < donation.full_amount:
            remaining_amount = donation.full_amount - total_invested
            invest_amount = min(
                remaining_amount,
                project.full_amount - project.invested_amount
            )
            project.invested_amount += invest_amount
            total_invested += invest_amount
            donation.invested_amount += invest_amount
            if project.invested_amount >= project.full_amount:
                project.fully_invested = True
                project.close_date = datetime.now()
            session.add(project)
            if donation.invested_amount >= donation.full_amount:
                donation.fully_invested = True
                donation.close_date = datetime.now()
            session.add(donation)
    await session.commit()
    await session.refresh(donation)
