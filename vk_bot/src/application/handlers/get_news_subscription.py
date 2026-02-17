from vkbottle import PhotoMessageUploader
from vkbottle.bot import BotLabeler, Message
from vkbottle.dispatch import BuiltinStateDispenser
from src.application.keyboards.miniapp_keyboard import get_miniapp_keyboard
from src.application.states import RegistrationStates
from src.services.interfaces import IUserService

router = BotLabeler()


@router.message(state=RegistrationStates.NEWS_SUBSCRIPTION)
async def get_news_sub(
        message: Message, user_service: IUserService,
        state_dispenser: BuiltinStateDispenser,
        photo_uploader: PhotoMessageUploader
):
    text = message.text.lower().strip() if message.text else ""
    if text not in ['да', 'нет']:
        await message.answer("Хотели бы вы получать новости? (Да/Нет)")
        return

    await user_service.update_news_subscription(message.from_id, (text == 'да'))
    await state_dispenser.delete(message.from_id)
    photo = await photo_uploader.upload('docs/sokol_like.webp', peer_id=message.peer_id)
    await message.answer(attachment=photo)
    await message.answer(
        "Спасибо! Ваша анкета сохранена. Вы можете воспользоваться нашим Mini App:",
        keyboard=get_miniapp_keyboard()
    )

