from sqlalchemy import Column, String, Text

from app.models.base import BaseInvestModel


class CharityProject(BaseInvestModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        base_repr = super().__repr__()
        project_repr = f', name={self.name}, description={self.description}'
        return base_repr[:-1] + project_repr + '}'
