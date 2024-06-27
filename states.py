# состояния
# старт
# - приветсвие
# - кнопки
# - команды
# - ссылки
#
# квест
# - кнопки
# -команды
#
# завершение викторины
# - кнопки
# - команды
# - интеграция с соцсетями
# - обратная связь

# Задача на текущий момент:
# сделать машину из двух состояний
# пользователь написал А - перевести машину в состояние А
# написал Б - перевести в Б
import telebot
from connect_to_bot import bot


greet = "приветствие"
quiz_rules = "и описание того, что щас будет викторина"
class State():
    def __init__(self):
        self.cur_state = None

class StateStart(State):
    def go_to_quiz(self):
        self.cur_state = StateQuiz()
    def go_to_end(self):
        self.cur_state = StateEnd()
    @bot.message_handler(commands=['start'])
    def greet(self, message):
        bot.send_message(message.chat.id, greet)
        chat_id = message.chat.id
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_support = telebot.types.KeyboardButton(text="Написать в поддержку")
        keyboard.add(button_support)
        bot.send_message(chat_id,
                         'Добро пожаловать в бота сбора обратной связи',
                         reply_markup=keyboard)
    @bot.message_handler(commands=['help'])
    def df(self):
        pass

class StateQuiz(State):
    def go_to_end(self):
        self.cur_state = StateEnd()
class StateEnd(State):
    def go_to_start(self):
        self.cur_state = StateStart()

