from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models import User
from app.schemas.donation import (
    DonationAdminResponse, DonationCreate, DonationResponse
)
from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.api.validators import validate_donation_amount


router = APIRouter()


@router.post('/', response_model=DonationResponse)
async def create_donation(
    donation: DonationCreate,
    session: Session = Depends(get_async_session),
    current_user: User = Depends(current_user)
):
    validate_donation_amount(donation.full_amount)
    new_donation = await donation_crud.create(donation, session, current_user)
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
