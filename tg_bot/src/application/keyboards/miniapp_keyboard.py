from aiogram.types import InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_miniapp_keyboard() -> InlineKeyboardMarkup:
    keyword = InlineKeyboardBuilder()
    keyword.button(text="Открыть сайт", web_app=WebAppInfo(url="https://ldpr.ru"))
    return keyword.as_markup()
