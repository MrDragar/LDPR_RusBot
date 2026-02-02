from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass
class User:
    id: int
    is_member: bool
    username: str | None
    surname: str
    name: str
    patronymic: str
    birth_date: date
    phone_number: str
    region: str
    email: str
    gender: str
    city: str
    wish_to_join: bool
    home_address: str | None
    news_subscription: bool = field(default=False)
    created_at: datetime = field(default_factory=lambda: datetime.now())
