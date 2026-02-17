import logging

from aiogram import Bot as TgBot
from vkbottle.bot import BotLabeler, Message
from vkbottle.dispatch import BuiltinStateDispenser

from src.application.handlers.finish_registration import finish_registration
from src.application.keyboards.boolean_keyboard import get_boolean_keyboard
from src.application.states import RegistrationStates
from src.services.interfaces import IUserService

router = BotLabeler()


@router.message(state=RegistrationStates.CITY)
async def get_city(
        message: Message, state_dispenser: BuiltinStateDispenser,
        user_service: IUserService, tg_bot: TgBot
):
    city = message.text.strip() if message.text else ""
    if len(city) < 2:
        return "Введите корректное название города."

    state = await state_dispenser.get(message.from_id)
    new_payload = {**state.payload, "city": city}
    logging.debug(new_payload)
    if new_payload['is_member']:
        await state_dispenser.set(message.from_id,
                                  RegistrationStates.HOME_ADDRESS,
                                  **new_payload)
        await message.answer(
            "Укажите ваш домашний адрес (улица, дом, квартира):")
    else:
        await finish_registration(
            user_service, message.from_id, new_payload,
            message.ctx_api, message.ctx_api.log_chat, state_dispenser,
            tg_bot
        )

        await state_dispenser.set(message.from_id,
                                  RegistrationStates.WISH_TO_JOIN,
                                  **new_payload)
        await message.answer("Хотите ли Вы присоединиться к команде ЛДПР?",
                             keyboard=get_boolean_keyboard())
