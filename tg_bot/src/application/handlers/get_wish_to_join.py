import logging

from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from src.application.handlers.finish_registration import finish_registration
from src.application.keyboards.boolean_keyboard import get_boolean_keyboard
from src.application.states import RegistrationStates
from src.services.interfaces import IUserService

router = Router(name=__name__)
logger = logging.getLogger(__name__)


@router.message(RegistrationStates.wish_to_join)
async def get_wish_to_join(
        message: types.Message, state: FSMContext, user_service: IUserService,
        log_chat: str
):
    answer = message.text.lower().strip()
    if not answer:
        return
    if answer not in ['да', 'нет']:
        await message.reply(
            "Хотите ли Вы присоединиться к команде ЛДПР?",
            reply_markup=get_boolean_keyboard()
        )
    logger.debug(f"Got wish to join: {answer}")
    await state.update_data(wish_to_join=(answer == 'да'))
    if answer == 'нет':
        return await finish_registration(user_service, state, message, log_chat)

    await message.reply('Для возможности направления документов укажите свой домашний адрес')
    await state.set_state(RegistrationStates.home_address)
