from fastapi import APIRouter

from app.api.endpoints import (
    charity_project_router,
    user_router
)

main_router = APIRouter()
main_router.include_router(
    charity_project_router, prefix='/meeting_rooms', tags=['Meeting Rooms'])
# main_router.include_router(
#     reservation_router, prefix='/reservations', tags=['Reservations'])
main_router.include_router(user_router)
