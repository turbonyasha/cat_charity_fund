from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Схема для создания и обновления CharityProject
class CharityProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)  # Название проекта (1-100 символов)
    description: str = Field(..., min_length=1)  # Описание проекта
    full_amount: int = Field(..., gt=0)  # Требуемая сумма (целое число больше 0)

class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)  # Название проекта
    description: Optional[str] = Field(None, min_length=1)  # Описание проекта
    full_amount: Optional[int] = Field(None, gt=0)  # Новая требуемая сумма (целое число больше 0)

class CharityProjectResponse(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
