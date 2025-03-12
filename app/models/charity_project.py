from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseInvestModel

FULL_INVEST = 'Полностью инвестирован'
NOT_FULL_INVEST = 'Идет сбор средств'


class CharityProject(BaseInvestModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    donations = relationship('Donation', back_populates='project')

    def __repr__(self):
        return (
            f"Проект '{self.name}' с объемом инвестиций {self.full_amount} "
            f"и суммой, уже инвестированной: {self.invested_amount}. "
            f"Описание: {self.description}. Статус: "
            f"{FULL_INVEST if self.fully_invested else NOT_FULL_INVEST}."
        )
