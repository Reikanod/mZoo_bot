import telebot
import os.path


class DevError(Exception):
    pass


if os.path.isfile(r'../token.txt'):
    path = r'../token.txt'
else:
    raise DevError("Путь к токену не найден")

with open(path, 'r') as file:
    TOKEN = file.read()

bot = telebot.TeleBot(TOKEN)