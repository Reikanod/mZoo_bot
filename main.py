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

@bot.message_handler(commands=['help', 'start'])
def start_info(message):
    text = f"""Здравствуй, {message.from_user.first_name.capitalize()}!
Расскажи о себе и своих предпочтениях и мы подберем тебе твое тотемное животное из \
Московского зоопарка!"""

    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def send(message):
    bot.reply_to(message, "fpfppf")




bot.polling()
