from app.models import Donation, CharityProject, User
from app.core.investment import invest_in_donation
from app.schemas.donation import DonationCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.crud.base import CRUDBase

class DonationCRUD(CRUDBase):

    async def create(self, obj_in: DonationCreate, session: AsyncSession, user: User) -> Donation:
        # Создаем пожертвование
        donation = await super().create(obj_in, session, user)

        # После создания пожертвования, запускаем процесс "инвестирования"
        await invest_in_donation(donation, session)

        return donation

    async def get_donations_for_user(self, user_id: int, session: AsyncSession) -> List[Donation]:
        # Получаем все пожертвования пользователя
        result = await session.execute(
            select(Donation).filter(Donation.user_id == user_id)
        )
        return result.scalars().all()

    async def get_all_donations(self, session: AsyncSession) -> List[Donation]:
        # Получаем все пожертвования, для суперпользователя
        result = await session.execute(select(Donation))
        return result.scalars().all()

    async def get_donation(self, obj_id: int, session: AsyncSession) -> Donation:
        # Получаем пожертвование по id
        return await super().get(obj_id, session)
    
    async def get_by_user(self, user_id: int, session: AsyncSession) -> List[Donation]:
        # Получаем пожертвования только для указанного пользователя
        donations = await session.execute(
            select(Donation).filter(Donation.user_id == user_id)
        )
        return donations.scalars().all()


donation_crud = DonationCRUD(Donation)