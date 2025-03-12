from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, root_validator

ALLOWED_FIELDS = {'name', 'description', 'full_amount'}
NON_CHANGE_FIELDS = 'Нельзя менять эти поля: {fields}'


class CharityProjectCreate(BaseModel):
    name: str = Field(..., max_length=100)
    description: str = Field(...)
    full_amount: int = Field(..., gt=0)

    class Config:
        min_anystr_length = 1


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None,)
    full_amount: Optional[int] = Field(None, gt=0)

    class Config:
        min_anystr_length = 1

    @root_validator(pre=True)
    def check_unexpected_fields(cls, values):
        allowed_fields = ALLOWED_FIELDS
        unexpected_fields = [field for field in values if (
            field not in allowed_fields)]
        if unexpected_fields:
            raise ValueError(
                NON_CHANGE_FIELDS.format(fields=', '.join(unexpected_fields)))
        return values


class CharityProjectResponse(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
