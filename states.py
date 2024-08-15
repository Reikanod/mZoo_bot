
import telebot
from connect_to_bot import bot


greet = "приветствие"
quiz_rules = "описание викторины"
class State():
    def __init__(self):
        self.cur_state = None

class StateStart(State):
    def go_to_quiz(self):
        self.cur_state = StateQuiz()
    def go_to_end(self):
        self.cur_state = StateEnd()



class StateQuiz(State):
    def go_to_end(self):
        self.cur_state = StateEnd()
class StateEnd(State):
    def go_to_start(self):
        self.cur_state = StateStart()

