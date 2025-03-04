from sqlalchemy.ext.asyncio import AsyncSession
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectCreate, CharityProjectUpdate, CharityProjectResponse
from app.core.investment import invest_in_project
from app.crud.base import CRUDBase

class CharityProjectCRUD(CRUDBase):
    def __init__(self):
        super().__init__(model=CharityProject)

    async def create(
            self,
            obj_in: CharityProjectCreate,
            session: AsyncSession,
    ):
        # Создаем новый проект с использованием базового метода create
        db_obj = await super().create(obj_in, session)

        # Инвестируем средства сразу после создания
        await invest_in_project(session, db_obj.id)

        return db_obj

    async def update(
            self,
            db_obj,
            obj_in: CharityProjectUpdate,
            session: AsyncSession,
    ):
        db_obj = await super().update(db_obj, obj_in, session)
        
        # Проверяем, если обновлены какие-то параметры и требуется перерасчет
        if db_obj.full_amount != db_obj.invested_amount:
            await invest_in_project(session, db_obj.id)
        
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        # Удаление возможно только если проект не имеет инвестированных средств
        if db_obj.invested_amount == 0:
            return await super().remove(db_obj, session)
        else:
            return None  # Если проект не пустой, его нельзя удалить
