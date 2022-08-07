from header import bot
import config
from user.user_funcs import *


def start(message):
    bot.send_message(message.chat.id, "Здравствуй, {0.first_name}!"
        .format(message.from_user, bot.get_me()))


def help(message):
    msg_to_user = config.HELP
    bot.send_message(message.chat.id, msg_to_user, parse_mode="html")


def encrypt(message):
    bot.send_message(message.chat.id, "Загрузи файл, который хочешь <b>зашифровать</b>", parse_mode="html")
    bot.register_next_step_handler(message, crypt_way)


def decrypt(message):
    bot.send_message(message.chat.id, "Загрузи файл, который хочешь <b>расшифровать</b>", parse_mode="html")
    bot.register_next_step_handler(message, crypt_way)