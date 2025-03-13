from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Donation
from app.crud.base import CRUDBase


class DonationCRUD(CRUDBase):

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
