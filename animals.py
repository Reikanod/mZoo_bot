# сюда сделать класс животных. Они должны иметь баллы по основным критериям
# человек должен по итогу иметь такие же свои баллы по тем же критериям и к кому он ближе
# то животное и порекомендовать

# здесь спарсить всех животных и к каждому указать ссылки на их странички, их имена
# главные их фотки и дополнительные, главная информация о них
#
import sqlite3
from bs4 import BeautifulSoup

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
        self.discription = '' # абзац с описанием животного

    def get_name(self):
        return self.name
    def set_name(self, a):
        self.name = a

    def get_page(self):
        return self.page
    def set_page(self, a):
        self.page = a

    def get_discription(self):
        return self.discription
    def set_discription(self, a):
        self.discription = a

    def get_criteria(self):
        return self.criteria
    def set_criteria(self, a):
        self.criteria = a

    def get_image(self):
        return self.image
    def set_image(self, a):
        self.image = a

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
)
''')


all_animals = []    # список из элементов класса Animal со всеми заполненными полями
print(all_tags_for_animals[1].find('img').get('src'))
for a in all_tags_for_animals:
    all_animals.append(Animal())
    name = a.find(class_='animal__name').get_text() # запоминаем имя животного
    page = a['href'] # запоминаем ссылку на животное
    img = a.find('img').get('src') # запоминаем ссылку на изображение животного

    all_animals[-1].set_name(name)
    all_animals[-1].set_page(page)
    all_animals[-1].set_image(img)
    all_animals[-1].set_discription('Описание животного')

i = 0
for an in all_animals:
    cursor.execute(f'''
INSERT INTO Animal
VALUES ({i}, {an.get_name()}, {an.get_page()}, {an.get_discription()}, )
''')
    i += 1





connection_to_sql.commit()
connection_to_sql.close()


