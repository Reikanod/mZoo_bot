# здесь будут собраны все вопросы для викторины



list_of_questions = {}        # создается словарь строка вопросов и список ответов к нему
with open(r'questions.txt', 'r', encoding='utf-8') as file:
    count = 1
    for line in file:
        if count == 1:
            prev_line = line
            count += 1
        else:
            list_of_questions[prev_line.strip()] = line.split(';')
            count = 1


