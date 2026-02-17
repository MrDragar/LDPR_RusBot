from vkbottle import Keyboard, OpenLink


def get_miniapp_keyboard():
    # В VK Mini App открывается через ссылку vk.com/app...
    return Keyboard(inline=True).add(OpenLink("https://плюссемь.рф", "Открыть сайт")).get_json()