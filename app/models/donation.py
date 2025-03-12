from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseInvestModel


class Donation(BaseInvestModel):
    project_id = Column(
        Integer, ForeignKey('charityproject.id'), nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)
    user = relationship('User', back_populates='donations')
    project = relationship('CharityProject', back_populates='donations')

    def __repr__(self):
        return (
            f"Пожертвование от пользователя {self.user_id} "
            f"для проекта '{self.project.name}' "
            f"в сумме {self.invested_amount}. "
            f"Комментарий: {self.comment or 'Без комментария'}."
        )
