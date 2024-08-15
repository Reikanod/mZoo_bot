# Задача скрипта - заполнить базу данных данными о всех животных
# Животные берутся с сайта зоопарка, записываются в локальную БД, в них заносятся все необходимые критерии для дальнейшей работы
import sqlite3
from bs4 import BeautifulSoup
import json
import requests
import random

# классы
class Animal:
    def __init__(self):
        self.name = '' # как называют этого животного на сайте
        self.criteria = criteria = { # личные критерии животного
            'hair' : 0, # есть ли шерсть у животного и настолько ее много
            'popular' : 0, # как много опекунов у животного уже есть
            'food' : 0, # 0 - травоядное, 5 - насекомые всякие и мелкие животные, 9 - хищник на крупную дичь
            'size' : 0, # размер животного
            'area' : 0, # район обитания. 0 - вода, 5 - земля, 9 - воздух
        }
        self.page = '' # адрес страницы этого животного
        self.image = '' # адрес изображения с этим животным
        self.description = '' # абзац с описанием животного

    def get_name(self):
        return self.name
    def set_name(self, a):
        self.name = a

    def get_page(self):
        return self.page
    def set_page(self, a):
        self.page = a

    def get_description(self):
        return self.description
    def set_description(self, a):
        self.description = a

    def get_criteria(self):
        return self.criteria
    def set_criteria(self, a):
        self.criteria = a

    def get_image(self):
        return self.image
    def set_image(self, a):
        self.image = a
# конец классов

# функции
def receive_ya_api_keys(): # получить необходимые ключи из файла
    with open(r'../ya_api_keys.txt', 'r', encoding='utf-8') as file:
        file_lines = file.readlines()
        cat_id = file_lines[1].strip()
        ya_api_id = file_lines[5].strip()
    keys = {
        'catalog_id': cat_id, # идентификатор каталога
        'ya_api_key': ya_api_id # ключ апишки
    }
    return keys

def ask_descr_from_yandex(keys, animal_name): # получить описание животного от яндекса. keys - словарь с ключами для апи, animal_name - имя животного с сайта зоопарка
    prompt = {
        "modelUri": f"gpt://{keys['catalog_id']}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": "В несколькоих предложениях опиши основную информацию об этом животном, степень редкости распространения, занесен ли в красную книгу"
            },
            {
                "role": "user",
                "text": animal_name
            }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {keys['ya_api_key']}"
    }

    response = requests.post(url, headers=headers, json=prompt)
    json_resp = response.text
    result = json.loads(json_resp)
    if result['result']: # если яндекс вернет результат - используем его. Если что то другое - результат равен пустой строке
        result = result['result']['alternatives'][0]['message']['text']
    else:
        result = ''
    return result

def first_info_into_bd(): # первый проход. В бд заносятся все животные и все возможные данные о них
    all_tags_for_animals = [] # тэги "а" с данными о животных сохранены в список
    with open(r'.\Жду опекуна.html', 'r', encoding='utf-8') as file: # достаю html код страницы из скачанного файла, так как спарсить сайт не дает
        soup = BeautifulSoup(file.read(), 'lxml')

    all_tags_for_animals = soup.findAll('a', class_='waiting-for-guardian-animals__item animal') # нашел все ссылки на животных

    connection_to_sql = sqlite3.connect('animals.db') # присоединяюсь к базе
    cursor = connection_to_sql.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Animals (
    id INTEGER PRIMARY KEY,
    name TEXT,
    page TEXT,
    discription TEXT,
    image TEXT,
    hair INTEGER,
    popular INTEGER,
    food INTEGER,
    size INTEGER,
    area INTEGER
    );
    ''')


    all_animals = []    # список из элементов класса Animal со всеми заполненными полями
    keys = receive_ya_api_keys() # получили ключи из файла
    for a in all_tags_for_animals:
        all_animals.append(Animal())
        name = a.find(class_='animal__name').get_text() # запоминаем имя животного
        page = a['href'] # запоминаем ссылку на животное
        img = a.find('img').get('src') # запоминаем ссылку на изображение животного
        description = ask_descr_from_yandex(keys, name) # запоминаем описание животного
        print(name, '////', page, '////', img)
        print(description.replace('\n', ' '))

        all_animals[-1].set_name(name) # запоминаем эту информацию в список из объектов класса Animal
        all_animals[-1].set_page(page)
        all_animals[-1].set_image(img)
        all_animals[-1].set_description(description.replace('\n', ' '))

    i = 1
    for an in all_animals: # проходимся по всем животным и в БД записываем о них всю информацию
        sql_query = f'''
    INSERT INTO Animals (id, name, page, discription, image, hair, popular, food, size, area)
    VALUES ({i}, '{an.get_name()}', '{an.get_page()}', '{an.get_description()}', '{an.get_image()}', 
    {an.get_criteria()['hair']}, {an.get_criteria()['popular']}, {an.get_criteria()['food']}, 
    {an.get_criteria()['size']}, {an.get_criteria()['area']});
    '''
        print(sql_query)
        cursor.execute(sql_query)
        i += 1

    connection_to_sql.commit()
    connection_to_sql.close() # коммичу и закрываю БД. В ней все данные о животных


def add_all_info_into_bd(): # дозаполнить все недостающие данные в бд
    connection_to_sql = sqlite3.connect('animals.db')
    cursor = connection_to_sql.cursor()
    sql_read = '''
    select * from Animals
    '''
    cursor.execute(sql_read)
    animals = cursor.fetchall() # здесь список из кортежей. Элементы списка - строки БД, кортежа - столбцы в строке
    criterias = ['hair', 'popular', 'food', 'size', 'area'] # для перебора критериев в цикле
    for an in animals:
        if not an[3]:  # если описания нет - получить описание у яндекса
            desc = ask_descr_from_yandex(keys, an[1])
            cursor.execute(f'''update Animals
            set discription = {desc}
            where name = "{an[1]}"''')
        for cr in criterias:
            sql_write_crit = f'''update Animals
            set {cr} = {random.randint(0, 9)}
            where name = "{an[1]}"
            '''
            cursor.execute(sql_write_crit)


    connection_to_sql.commit()
    connection_to_sql.close()




# конец функций

# main
keys = receive_ya_api_keys()
#first_info_into_bd()
#add_all_info_into_bd()




