from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Donation, User
from app.services.investment import invest
from app.schemas.donation import DonationCreate
from app.models import CharityProject
from app.crud.base import CRUDBase


class DonationCRUD(CRUDBase):
    async def create(
        self,
        donation: DonationCreate,
        session: AsyncSession,
        user: User
    ) -> Donation:
        new_donation = await super().create(donation, session, user)
        sources = await session.execute(
            select(CharityProject).filter(
                CharityProject.fully_invested.is_(False))
        )
        sources = sources.scalars().all()
        target, changed_sources = invest(new_donation, sources)
        session.add(target)
        if changed_sources:
            session.add_all(changed_sources)
        await session.commit()
        await session.refresh(target)
        return new_donation

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
