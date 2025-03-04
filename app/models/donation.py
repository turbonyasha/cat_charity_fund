from sqlalchemy import Column, Integer, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base import BaseInvestModel


class Donation(BaseInvestModel):
    # Здесь добавляется внешний ключ, который связывает поле `project_id` с таблицей CharityProject
    project_id = Column(Integer, ForeignKey("charityproject.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    comment = Column(Text, nullable=True)

    user = relationship("User", back_populates="donations")
    project = relationship("CharityProject", back_populates="donations")
