import requests
import json

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
keys = receive_ya_api_keys()
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
                "text": "Одной цифрой от 0 до 9 оцени длину шерсти у животного. По любым критериям. В ответе нужна только одна цифра. О - нет шерсти. 9 - пушистый как песец"
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

print(ask_descr_from_yandex(keys, "жираф"))
print(ask_descr_from_yandex(keys, "слон"))
print(ask_descr_from_yandex(keys, "мышь"))
print(ask_descr_from_yandex(keys, "морской котик"))