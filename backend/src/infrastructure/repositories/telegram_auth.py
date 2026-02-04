from aiogram.utils.web_app import safe_parse_webapp_init_data, check_webapp_signature, WebAppInitData

from src.domain.exceptions import AuthError
from src.domain.interfaces import ITelegramAuthRepository


class AiogramTelegramAuthRepository(ITelegramAuthRepository):
    _token: str

    def __init__(self, token: str):
        self._token = token

    async def verify_data(self, auth_data: str) -> int:
        try:
            init_data: WebAppInitData = await safe_parse_webapp_init_data(
                self._token, auth_data
            )
        except ValueError:
            raise AuthError("Некорректные данные авторизации")
        except Exception as e:
            raise AuthError(f"Неизвестная ошибка {e}")
        return init_data.user.id
