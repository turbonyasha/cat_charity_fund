from app.models import CharityProject, Donation
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime


async def invest_in_project(project: CharityProject, session: AsyncSession):
    # Автоматически распределяем средства из пожертвований на новый проект
    donations = await session.execute(select(Donation).filter(Donation.fully_invested == False))
    donations = donations.scalars().all()

    total_invested = 0
    for donation in donations:
        # Распределяем средства из пожертвования в проект
        if total_invested < project.full_amount:
            remaining_amount = project.full_amount - total_invested
            invest_amount = min(donation.full_amount - donation.invested_amount, remaining_amount)

            donation.invested_amount += invest_amount
            total_invested += invest_amount
            donation.fully_invested = donation.invested_amount == donation.full_amount
            if donation.fully_invested:
                donation.close_date = datetime.utcnow()

            # Если проект уже собрал необходимую сумму, устанавливаем его как полностью финансируемый
            if total_invested >= project.full_amount:
                project.fully_invested = True
                project.close_date = datetime.utcnow()

            session.add(donation)

    # Обновление состояния проекта после перераспределения средств
    if total_invested > 0:  # Проверка, что хотя бы что-то было инвестировано
        project.invested_amount = total_invested
        if project.invested_amount >= project.full_amount:
            project.fully_invested = True
            project.close_date = datetime.utcnow()

    # Если проект полностью закрыт, обновляем его статус
    session.add(project)

    # Завершаем транзакцию
    await session.commit()
    await session.refresh(project)



async def invest_in_donation(donation: Donation, session: AsyncSession):
    # Ищем все проекты, которые еще не закрыты
    projects = await session.execute(select(CharityProject).filter(CharityProject.fully_invested == False))
    projects = projects.scalars().all()

    total_invested = 0
    for project in projects:
        # Инвестируем средства из пожертвования в проект
        if total_invested < donation.full_amount:
            remaining_amount = donation.full_amount - total_invested
            invest_amount = min(remaining_amount, project.full_amount - project.invested_amount)

            project.invested_amount += invest_amount
            total_invested += invest_amount
            donation.invested_amount += invest_amount

            if project.invested_amount >= project.full_amount:
                project.fully_invested = True
                project.close_date = datetime.utcnow()

            session.add(project)
            if donation.invested_amount >= donation.full_amount:
                donation.fully_invested = True
                donation.close_date = datetime.utcnow()

            session.add(donation)

    await session.commit()
    await session.refresh(donation)