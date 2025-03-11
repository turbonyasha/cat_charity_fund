from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DonationResponse(BaseModel):
    id: int
    full_amount: int
    comment: Optional[str] = None
    create_date: datetime

    class Config:
        orm_mode = True


class DonationAdminResponse(BaseModel):
    id: int
    full_amount: int
    invested_amount: int
    fully_invested: bool
    comment: Optional[str] = None
    create_date: datetime
    close_date: Optional[datetime] = None
    user_id: int

    class Config:
        orm_mode = True


class DonationCreate(BaseModel):
    full_amount: int
    comment: Optional[str] = None

    class Config:
        orm_mode = True
