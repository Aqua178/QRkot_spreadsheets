from typing import Union, Optional

from fastapi import Depends, Request
from fastapi_users import (IntegerIDMixin, BaseUserManager,
                           InvalidPasswordException, FastAPIUsers)
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate


PASSWORD_TO_SHORT = 'Password should be at least 3 characters'
EMAIL_IN_PASSWORD = 'Password should not contain e-mail'
USER_REGISTERED = 'Пользователь {} зарегистрирован.'
LIFETIME_SECONDS = 3600
SHORT_PASSWORD = 6


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret, lifetime_seconds=LIFETIME_SECONDS)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def validate_password(
            self,
            password: str,
            user: Union[UserCreate, User],
    ) -> None:
        if len(password) < SHORT_PASSWORD:
            raise InvalidPasswordException(
                reason=PASSWORD_TO_SHORT
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason=EMAIL_IN_PASSWORD
            )

    async def on_after_register(
            self, user: User, request: Optional[Request] = None
    ):
        print(USER_REGISTERED.format(user.email))


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
