from vkbottle import Keyboard, OpenLink


def get_miniapp_keyboard():
    # В VK Mini App открывается через ссылку vk.com/app...
    return Keyboard(inline=True).add(OpenLink("https://ldpr.ru/", "Открыть сайт")).get_json()