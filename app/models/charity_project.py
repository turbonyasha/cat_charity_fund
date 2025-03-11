from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseInvestModel


class CharityProject(BaseInvestModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    donations = relationship('Donation', back_populates='project')
