from src.domain.entities import User
from src.domain.exceptions import UserNotFoundError, AuthError, AuthBadUserError
from src.domain.interfaces import IUserRepository, ITelegramAuthRepository, \
    IJWTRepository, IUnitOfWork
from src.services.interfaces import IAuthService


class AuthService(IAuthService):
    def __init__(
            self,
            user_repository: IUserRepository,
            telegram_auth_repository: ITelegramAuthRepository,
            jwt_repository: IJWTRepository,
            uow: IUnitOfWork
    ):
        self.__user_repository = user_repository
        self.__telegram_auth_repository = telegram_auth_repository
        self.__jwt_repository = jwt_repository
        self.__uow = uow

    async def authenticate(self, auth_data: str) -> str:
        if not auth_data:
            raise AuthError("Пустые данные авторизации")
        try:
            user_id = await self.__telegram_auth_repository.verify_data(auth_data)
            with self.__uow.atomic():
                user = await self.__user_repository.get_user(user_id)
            jwt_token = await self.__jwt_repository.create_access_token(user)
        except UserNotFoundError:
            raise AuthBadUserError("Такой пользователь не найден")
        except AuthError:
            raise
        except Exception:
            raise AuthError('Неизвестная ошибка авторизации')
        return jwt_token

    async def get_user(self, jwt_token: str) -> User:
        if not jwt_token:
            raise AuthError('Пустой JWT токе')
        try:
            token_user = await self.__jwt_repository.decode_access_token(jwt_token)
            with self.__uow.atomic():
                user = await self.__user_repository.get_user(token_user.id)
        except UserNotFoundError:
            raise AuthBadUserError('Такого пользователя не существует')
        except Exception:
            raise AuthError('Неизвестная ошибка авторизации')
        return user
