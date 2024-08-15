import telebot.types

from connect_to_bot import bot
from states import State, StateStart
from quiz import list_of_questions

state = State()
state.cur_state = StateStart()


@bot.message_handler(commands=['start'])
def greet(message):
    state.cur_state = 'start'
def greet_dialog(message):
    pass


@bot.message_handler(commands=['quiz'])
def quiz(message):
    state.cur_state = 'quiz'
    keyboard = telebot.types.ReplyKeyboardMarkup()
    button_start_quiz = telebot.types.KeyboardButton('Начать викторину')
    keyboard.add(button_start_quiz)
    bot.send_message(message.chat.id, "Ответьте на вопросы и мы подберем ваше тотемное животной из нашего зоопарка", reply_markup=keyboard)

def quiz_dialog(message):
    questions = list_of_questions.copy()
    question = questions.popitem()
    keyboard = telebot.types.ReplyKeyboardMarkup()
    for answer in question:
        telebot.types.KeyboardButton(answer)
        keyboard.add(answer)



@bot.message_handler(content_types=['text'])
def state(message):
    match state.cur_state:
        case 'start':
            greet_dialog(message)
        case 'quiz':
            quiz_dialog(message)









bot.polling()
