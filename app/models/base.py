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
            'invested_amount <= full_amount', name='check_invested_amount'),
    )
