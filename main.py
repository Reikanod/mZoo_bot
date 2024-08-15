from connect_to_bot import bot
from states import State, StateStart


state = State()
state.cur_state = StateStart()


@bot.message_handler(commands=['start'])
def greet(message):
    state.cur_state = 'start'

def greet_dialog(message):
    pass

@bot.message_handler(content_types=['text'])
def state(message):
    match state.cur_state:
        case 'start':
            greet_dialog(message)










bot.polling()
