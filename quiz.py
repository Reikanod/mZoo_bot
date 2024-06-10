# здесь будут собраны все вопросы для викторины
path_to_questions = r'questions.txt'


class Quiz():
    def __init__(self):
        self.path_to_questions = path_to_questions
        self.list_of_questions = {}
        # создается словарь из вопросов и ответов к нему

    def read_questions(self):  # обновляет список вопросов, считывая их из файла
        with open(path_to_questions, 'r') as file:
            for line in file:
                if line[0] == '#' or not line:
                    continue
                

class Questions():
    def __init__(self):
        self.question = ''
        self.answers = []
        # считать вопросы из файла

    def # функция, которая результаты ответов пользователя