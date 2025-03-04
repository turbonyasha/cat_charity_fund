from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base import BaseInvestModel


class CharityProject(BaseInvestModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    # Связь с пожертвованиями
    donations = relationship("Donation", back_populates="project")