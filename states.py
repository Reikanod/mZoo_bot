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

