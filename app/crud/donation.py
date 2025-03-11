from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Donation, User
from app.core.investment import invest_donation
from app.schemas.donation import DonationCreate
from app.crud.base import CRUDBase


class DonationCRUD(CRUDBase):
    async def create(
        self,
        donation: DonationCreate,
        session: AsyncSession,
        user: User
    ) -> Donation:
        new_donation = await super().create(donation, session, user)
        await invest_donation(new_donation, session)
        return new_donation

    async def get_donations_for_user(
        self,
        user_id: int,
        session: AsyncSession
    ) -> list[Donation]:
        result = await session.execute(
            select(Donation).filter(Donation.user_id == user_id)
        )
        return result.scalars().all()

    async def get_all_donations(self, session: AsyncSession) -> list[Donation]:
        result = await session.execute(select(Donation))
        return result.scalars().all()

    async def get_donation(
        self,
        donation_id: int,
        session: AsyncSession
    ) -> Donation:
        return await super().get(donation_id, session)

    async def get_by_user(
        self,
        user_id: int,
        session: AsyncSession
    ) -> list[Donation]:
        donations = await session.execute(
            select(Donation).filter(Donation.user_id == user_id)
        )
        return donations.scalars().all()


donation_crud = DonationCRUD(Donation)
