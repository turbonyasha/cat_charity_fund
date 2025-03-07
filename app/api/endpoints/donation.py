from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Donation, User
from app.schemas.donation import DonationAdminResponse, DonationCreate, DonationResponse
from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud

router = APIRouter()


@router.post('/', response_model=DonationResponse)
async def create_donation(
    donation: DonationCreate,
    session: Session = Depends(get_async_session),
    current_user: User = Depends(current_user)
):
    # Проверяем, что сумма пожертвования больше 0
    if donation.full_amount <= 0:
        raise HTTPException(status_code=400, detail="Donation amount must be greater than 0")

    # Создаем пожертвование через CRUD
    new_donation = await donation_crud.create(donation, session, current_user)

    # Запускаем процесс инвестирования после создания пожертвования
    # await invest_funds(new_donation, session)

    return new_donation


@router.get("/", response_model=list[DonationAdminResponse])
async def get_all_donations(db: Session = Depends(get_async_session), current_user: User = Depends(current_user)):
    # Проверяем, является ли текущий пользователь суперпользователем
    if not current_superuser(current_user):
        raise HTTPException(status_code=403, detail="You don't have permission to view all donations")
    
    # Получаем все пожертвования через CRUD
    donations = await donation_crud.get_multi(db)
    return donations


@router.get("/my", response_model=list[DonationResponse])
async def get_my_donations(db: Session = Depends(get_async_session), current_user: User = Depends(current_user)):
    # Получаем только пожертвования текущего пользователя через CRUD
    donations = await donation_crud.get_by_user(current_user.id, db)
    return donations
