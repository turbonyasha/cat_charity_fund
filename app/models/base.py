from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
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

    # @classmethod
    # def __tablename__(cls):
    #     return ''.join(['_' + i.lower() if i.isupper() else i for i in cls.__name__]).lstrip('_')