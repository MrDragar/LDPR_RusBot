from aiogram import Bot as TgBot
from vkbottle.bot import BotLabeler, Message
from vkbottle.dispatch import BuiltinStateDispenser

from src.application.handlers.finish_registration import finish_registration
from src.application.states import RegistrationStates
from src.services.interfaces import IUserService

router = BotLabeler()


@router.message(state=RegistrationStates.HOME_ADDRESS)
async def get_home_address(
        message: Message, user_service: IUserService,
        state_dispenser: BuiltinStateDispenser,
        tg_bot: TgBot
):
    if not message.text: return

    state = await state_dispenser.get(message.from_id)
    new_payload = {**state.payload, "home_address": message.text.strip()}

    await finish_registration(
        user_service, message.from_id, new_payload,
        message.ctx_api, message.ctx_api.log_chat, state_dispenser, tg_bot
    )
