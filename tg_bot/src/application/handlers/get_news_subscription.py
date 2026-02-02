import logging

from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from src.application.keyboards.boolean_keyboard import get_boolean_keyboard
from src.application.states import RegistrationStates
from src.services.interfaces import IUserService

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(RegistrationStates.news_subscription)
async def get_news_subscription(message: types.Message, state: FSMContext, user_service: IUserService, log_chat: str):
    answer = message.text.lower().strip()
    if not answer:
        return
    if answer not in ['да', 'нет']:
        await message.reply(
            "Хотели бы вы получать информацию о инициативах и мероприятиях ЛДПР?",
            reply_markup=get_boolean_keyboard()
        )
    logger.debug(f"Got news_subscription: {answer}")
    await user_service.update_news_subscription(
        message.from_user.id, answer == 'да'
    )
    await state.clear()
    await message.answer_sticker(types.FSInputFile('docs/sokol_like.webp'))
