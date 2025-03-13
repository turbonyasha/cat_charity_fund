from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models import User, CharityProject
from app.schemas.donation import (
    DonationAdminResponse, DonationCreate, DonationResponse
)
from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.api.validators import validate_donation_amount
from app.services.investment import invest


router = APIRouter()


@router.post('/', response_model=DonationResponse)
async def create_donation(
    donation: DonationCreate,
    session: Session = Depends(get_async_session),
    current_user: User = Depends(current_user)
):
    validate_donation_amount(donation.full_amount)
    new_donation = await donation_crud.create(
        donation,
        session,
        current_user,
        commit=False
    )
    sources = await donation_crud.get_non_invested_sources(
        session, model=CharityProject
    )
    changed_sources = invest(new_donation, sources)
    session.add_all(changed_sources)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/',
    response_model=list[DonationAdminResponse],
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(session: Session = Depends(get_async_session)):
    return await donation_crud.get_multi(session)


@router.get('/my', response_model=list[DonationResponse])
async def get_my_donations(
    session: Session = Depends(get_async_session),
    current_user: User = Depends(current_user)
):
    return await donation_crud.get_by_user(current_user.id, session)
