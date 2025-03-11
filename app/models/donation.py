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
