from aiogram.types import InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_miniapp_keyboard() -> InlineKeyboardMarkup:
    keyword = InlineKeyboardBuilder()
    keyword.button(text="🚀 Открыть Mini App", web_app=WebAppInfo(url="https://плюссемь.рф"))
    return keyword.as_markup()
