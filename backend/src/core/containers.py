from src.core.di import DeclarativeContainer, providers
from src.domain.interfaces import IUnitOfWork, IUserRepository, \
    IStringSorterRepository, IJWTRepository, ITelegramAuthRepository
from src.infrastructure import Database, UnitOfWork
from src.infrastructure.interfaces import IDatabase
from src.infrastructure.repositories import (
    UserRepository,
    AiogramTelegramAuthRepository, JWTRepository
)
from src.core import config
from src.services import UserService, AuthService
from src.services.interfaces import IUserService, IAuthService


class Container(DeclarativeContainer):
    database: providers.Singleton[IDatabase] = providers.Singleton(
        Database, "db.sqlite3"
    )
    uow: providers.Singleton[IUnitOfWork] = providers.Singleton(
        UnitOfWork, database=database
    )
    user_repository: providers.Factory[IUserRepository] = providers.Factory(
        UserRepository, uow=uow
    )
    jwt_repository: providers.Factory[IJWTRepository] = providers.Factory(
        JWTRepository, secret_key=config.SECRET_KEY, algorithm=config.ALGORITHM
    )
    telegram_auth_repository: (
        providers.Factory)[ITelegramAuthRepository] = providers.Factory(
        AiogramTelegramAuthRepository, config.BOT_TOKEN
    )
    user_service: providers.Factory[IUserService] = providers.Factory(
        UserService, user_repo=user_repository, uow=uow
    )
    auth_service: providers.Factory[IAuthService] = providers.Factory(
        AuthService, user_repository=user_repository,
        telegram_auth_repository=telegram_auth_repository,
        jwt_repository=jwt_repository,
        uow=uow
    )
