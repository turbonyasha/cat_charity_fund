from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseInvestModel


class Donation(BaseInvestModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)
    user = relationship('User', back_populates='donations')

    def __repr__(self):
        base_repr = super().__repr__()
        donation_repr = (
            f'user_id={self.user_id}, '
            f"comment={self.comment if self.comment else 'None'}"
        )
        return base_repr[:-1] + donation_repr + '}'
