# app/api/endpoints/user.py
from fastapi import APIRouter

from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()

router.include_router(
    # В роутер аутентификации
    # передается объект бэкенда аутентификации.
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)
# router.include_router(
#     fastapi_users.get_users_router(UserRead, UserUpdate),
#     prefix='/users',
#     tags=['users'],
# )
# Сохраняем роутер в переменную.
users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
# Из списка эндпоинтов роутера исключаем ненужную ручку.
users_router.routes = [
    rout for rout in users_router.routes if rout.name != 'users:delete_user'
]
# Подключаем изменённый роутер по старому адресу.
router.include_router(
    users_router,
    prefix='/users',
    tags=['users'],
)
