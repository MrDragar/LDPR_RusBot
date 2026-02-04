import logging
from datetime import timedelta, datetime, UTC
from typing import Optional
from dataclasses import asdict

from jose import jwt

from src.domain.entities import User
from src.domain.exceptions import AuthError
from src.domain.interfaces import IJWTRepository


class JWTRepository(IJWTRepository):
    __secret_key: str
    __algorithm: str

    def __init__(self, secret_key, algorithm):
        self.__secret_key = secret_key
        self.__algorithm = algorithm

    async def create_access_token(
        self, user: User, expires_delta: Optional[timedelta] = None
    ) -> str:
        if expires_delta is None:
            expires_delta = timedelta(minutes=30)
        expire = datetime.now(UTC) + expires_delta
        data = asdict(user)
        del data["created_at"]
        del data["birth_date"]
        data["exp"] = int(expire.timestamp())
        return jwt.encode(data, self.__secret_key, algorithm=self.__algorithm)

    async def decode_access_token(self, token: str) -> int:
        payload = jwt.decode(token, self.__secret_key, algorithms=[self.__algorithm])
        if int(payload.get('exp')) < datetime.now(UTC).timestamp():
            raise AuthError('Токен истёк')
        if 'id' not in payload:
            raise AuthError('Некорректный токен')
        return payload['id']


