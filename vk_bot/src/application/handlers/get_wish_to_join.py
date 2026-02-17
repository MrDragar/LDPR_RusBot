from vkbottle.bot import BotLabeler, Message
from vkbottle.dispatch import BuiltinStateDispenser
from aiogram import Bot as TgBot

from src.application.handlers.finish_registration import finish_registration
from src.application.keyboards.boolean_keyboard import get_boolean_keyboard
from src.application.states import RegistrationStates
from src.services.interfaces import IUserService

router = BotLabeler()


@router.message(state=RegistrationStates.WISH_TO_JOIN)
async def get_wish(
        message: Message, user_service: IUserService,
        state_dispenser: BuiltinStateDispenser, tg_bot: TgBot
):
    text = message.text.lower().strip() if message.text else ""
    if text not in ['да', 'нет']:
        await message.answer("Выберите вариант 'Да' или 'Нет':",
                             keyboard=get_boolean_keyboard())
        return

    state = await state_dispenser.get(message.from_id)
    new_payload = {**state.payload, "wish_to_join": (text == 'да')}

    if text == 'нет':
        await finish_registration(
            user_service, message.from_id, new_payload,
            message.ctx_api, message.ctx_api.log_chat, state_dispenser,
            tg_bot
        )
    else:
        await state_dispenser.set(
            message.from_id,
            RegistrationStates.HOME_ADDRESS,
            **new_payload
        )
        await message.answer(
            "Для вступления в команду укажите ваш домашний адрес:")
