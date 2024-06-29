from connect_to_bot import bot
from states import State, StateStart


state = State()
state.cur_state = StateStart()


@bot.message_handler(commands=['start'])
def greet(message):
    state.cur_state.greet(message)










bot.polling()
