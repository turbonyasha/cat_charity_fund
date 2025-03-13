from app.models import CharityProject
from .base import CRUDBase


class CharityProjectCRUD(CRUDBase):
    pass


charity_project_crud = CharityProjectCRUD(CharityProject)
