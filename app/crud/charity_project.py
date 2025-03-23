from operator import itemgetter

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from app.models import CharityProject
from .base import CRUDBase


class CharityProjectCRUD(CRUDBase):
    async def get_projects_by_completion_rate(
        self, session: AsyncSession
    ) -> list[dict[str, str]]:
        result = await session.execute(
            select(
                CharityProject.name,
                CharityProject.create_date,
                CharityProject.close_date,
                CharityProject.description,
                (func.julianday(
                    CharityProject.close_date) - func.julianday(
                        CharityProject.create_date))
            ).where(
                CharityProject.fully_invested is True,
                CharityProject.close_date is not None
            )
        )
        projects_with_duration = []
        for project in result.all():
            name, _, _, description, duration_in_days = project
            total_seconds = duration_in_days * 24 * 60 * 60
            days = int(total_seconds // (24 * 3600))
            total_seconds %= (24 * 3600)
            hours = int(total_seconds // 3600)
            total_seconds %= 3600
            minutes = int(total_seconds // 60)
            total_seconds %= 60
            seconds = int(total_seconds)
            duration_str = str(timedelta(
                days=days, hours=hours, minutes=minutes, seconds=seconds))
            projects_with_duration.append({
                'name': name,
                'duration': duration_str,
                'description': description,
                'total_seconds': total_seconds
            })
        projects_with_duration.sort(key=itemgetter('total_seconds'))
        for project in projects_with_duration:
            del project['total_seconds']
        return projects_with_duration


charity_project_crud = CharityProjectCRUD(CharityProject)
