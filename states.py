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

class States():
    def __init__(self):
        self.state = ''

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

class stateA(States):
    def __init__(self):
        self.set_state('A')

    def go_to_b(self):
        self.set_state('B')

class stateB(States):
    def __init__(self):
        self.set_state('B')

    def go_to_b(self):
        self.set_state('A')