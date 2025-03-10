from pydantic import BaseModel, Field, ValidationError, root_validator
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

    @root_validator(pre=True)
    def check_unexpected_fields(cls, values):
        allowed_fields = {'name', 'description', 'full_amount'}
        unexpected_fields = [field for field in values if field not in allowed_fields]
        if unexpected_fields:
            raise ValueError(f"Unexpected fields: {', '.join(unexpected_fields)}")
        return values

class CharityProjectResponse(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
