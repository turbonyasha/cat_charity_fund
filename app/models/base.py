from sqlalchemy import Column, Integer, Boolean, DateTime, CheckConstraint
from datetime import datetime

from app.core.db import Base


class BaseInvestModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint(
            'full_amount > 0', name='check_full_amount_positive'),
        CheckConstraint(
            '0 <= invested_amount <= full_amount',
            name='check_invested_amount_range'
        ),
    )

    def __repr__(self):
        return (
            f'<{self.__class__.__name__}('
            f'id={self.id}, '
            f'full_amount={self.full_amount}, '
            f'invested_amount={self.invested_amount}, '
            f'fully_invested={self.fully_invested}, '
            f'create_date={self.create_date}, '
            f'close_date={self.close_date})>'
        )
