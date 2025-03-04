from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Donation
from app.schemas import DonationCreate, DonationUpdate
from app.crud import CRUDBase



class DonationCRUD(CRUDBase):
    def __init__(self):
        super().__init__(model=Donation)

    async def create(
            self,
            obj_in: DonationCreate,
            session: AsyncSession,
    ):
        # Создаем пожертвование
        db_obj = await super().create(obj_in, session)

        # После создания пожертвования, автоматически увеличиваем invested_amount у проекта
        await self._update_project_investment(session, db_obj.project_id, db_obj.amount)

        return db_obj

    async def update(
            self,
            db_obj,
            obj_in: DonationUpdate,
            session: AsyncSession,
    ):
        # Обновление пожертвования
        db_obj = await super().update(db_obj, obj_in, session)

        # После обновления, пересчитываем вклад в проект
        await self._update_project_investment(session, db_obj.project_id, db_obj.amount)

        return db_obj

    async def _update_project_investment(self, session: AsyncSession, project_id: int, amount: int):
        # Логика для обновления суммы, внесенной в проект
        project = await session.execute(select(Donation).where(Donation.project_id == project_id))
        project = project.scalars().first()

        if not project:
            return None

        # Добавляем средства в проект
        project.invested_amount += amount
        if project.invested_amount >= project.full_amount:
            project.fully_invested = True
            project.close_date = datetime.utcnow()

        # Сохраняем изменения
        await session.commit()
        await session.refresh(project)
        return project
