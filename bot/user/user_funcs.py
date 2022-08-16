import os
import time
from dataclasses import dataclass
import utils
from header import bot
from telebot import types
import user.fernet as fernet


@dataclass
class File():
    name: str
    bytes: bytes
    password: str = ""


@dataclass
class TgFile():
    file_name: str
    file_id: str
    file_size: int
    file_path: str


keyboard = types.ReplyKeyboardMarkup(True)
keyboard.add("Отмена")


def crypt_way(message):
    if message.content_type == "text" and message.text.lower() == "отмена":
        _brake(message)
    else:
        get_file(message)


def get_file(message) -> None:
    if message.content_type == "text":
        text = message.text
        file_name = "text_file.txt"
        bytes = text.encode('utf-8')
    else:
        tgFile = catch_file_type(message)
        if tgFile == None: # file_size > 20mb or something
            bot.send_message(message.chat.id, "Не могу загрузить файл")
            return None
        else:
            file_name = tgFile.file_name
            bytes = bot.download_file(tgFile.file_path)
    file = File(file_name, bytes)
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "Теперь напиши пароль 🙈:", parse_mode="html", reply_markup=keyboard)

    bot.register_next_step_handler(message, _get_password, file)


def catch_file_type(message):
    try:
        file_name = None
        if message.content_type == "photo":
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        elif message.content_type == "video":
            file_info = bot.get_file(message.video.file_id)
        elif message.content_type == "video_note":
            file_info = bot.get_file(message.video_note.file_id)
        elif message.content_type == "voice":
            file_info = bot.get_file(message.voice.file_id)
        elif message.content_type == "audio":
            file_info = bot.get_file(message.audio.file_id)
            file_name = message.audio.file_name
        # elif message.content_type == "sticker":
        #     file_info = bot.get_file(message.sticker.file_id)
        else: # document type
            file_info = bot.get_file(message.document.file_id)
            file_name = message.document.file_name

        if not file_name:
            file_name = file_info.file_path.split("/")[1]
        return TgFile(file_name, file_info.file_id, file_info.file_size, file_info.file_path)
    except Exception as e:
        print(e)
        return None


def _brake(message):
    bot.send_message(message.chat.id, "Отменено", reply_markup=types.ReplyKeyboardRemove())


def _get_password(message, file: File) -> None:
    if message.text.lower() == "отмена":
        _brake(message)
    else:
        file.password = message.text
        bot.delete_message(message.chat.id, message.message_id)
        if file.name.split(".")[-1] == "enc":
            _send_dec_file(message, file)
        else:
            _send_enc_file(message, file)


def _write_file(name, bytes):
    src = "../temp/"
    with open(src + name, 'wb') as new_file:
        new_file.write(bytes)
    return new_file


def _send_enc_file(message, file: File) -> None:
    bot.send_chat_action(message.chat.id, 'upload_document')

    file.name += ".enc"
    enc_bytes = _encrypted_file(file)
    packed_file = _write_file(file.name, enc_bytes)

    bot.send_document(message.chat.id, open(packed_file.name), reply_markup=types.ReplyKeyboardRemove())
    os.remove(packed_file.name)


def _send_dec_file(message, file: File) -> None:
    dec_bytes = _decrypted_file(file)
    if dec_bytes == None:
        bot.send_message(message.chat.id, "Упс! Похоже, что пароль не верен, попробуй снова!", parse_mode="html", reply_markup=keyboard)
        bot.register_next_step_handler(message, _get_password, file)
    else:
        bot.send_chat_action(message.chat.id, 'upload_document')
        file.name = file.name[0:-4]
        packed_file = _write_file(file.name, dec_bytes)
        msg = bot.send_document(message.chat.id, open(packed_file.name, 'rb'), caption="Файл будет удален по истечении 1 минуты", reply_markup=types.ReplyKeyboardRemove())
        os.remove(packed_file.name)
        time.sleep(60)
        bot.delete_message(message.chat.id, msg.message_id)


def _encrypted_file(file: File):
    enc_file = fernet.encrypted(file.bytes, file.password)
    return enc_file


def _decrypted_file(file: File):
    dec_file = fernet.decrypted(file.bytes, file.password)
    return dec_file

