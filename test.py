import requests
import json
from bs4 import BeautifulSoup


req_text = input()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
}

params = {
    'q': req_text,
    'client': 'psy-ab',
    'gs_ri': 'gws-wiz',
}

res = requests.get("https://www.google.com/search", params=params, headers=headers)
result = res.text # html код страницы с ответом(наверное)
soup = BeautifulSoup(result, 'lxml')
html_resp_from_google = str(soup) # ответ от гугла по нашему запросу
all_span_tags = soup.find('div', id="kp-wp-tab-overview").find_all('span') # все спаны в нужном нам диве

list_of_spans_texts = []
for span in all_span_tags:
    list_of_spans_texts.append(span.get_text())
    if not list_of_spans_texts[-1] or len(list_of_spans_texts[-1]) < 150:
        list_of_spans_texts.pop()

with open(r'C:\Users\dfjgh\Desktop\f.txt', 'w', encoding='utf-8') as file:
    for el in list_of_spans_texts:
        file.writelines(str(el).replace('...', ''))

text = str(list_of_spans_texts)

with open(r'../ya_api_keys.txt', 'r', encoding='utf-8') as file:
    file_lines = file.readlines()
    cat_id = file_lines[1].strip()
    ya_api_id = file_lines[5].strip()


prompt = {
    "modelUri": f"gpt://{cat_id}/yandexgpt-lite",
    "completionOptions": {
        "stream": False,
        "temperature": 0.6,
        "maxTokens": "2000"
    },
    "messages": [
        {
            "role": "system",
            "text": "Перефразируй текст, убери лишнее, повторения, технические детали, не относящуюся к животному информацию"
        },
        {
            "role": "user",
            "text": text
        }
    ]
}


url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Api-Key {ya_api_id}"
}

response = requests.post(url, headers=headers, json=prompt)
json_resp = response.text
result = json.loads(json_resp)
print(type(result))
result = result['result']['alternatives'][0]['message']['text']
print(type(result))
print(result)


