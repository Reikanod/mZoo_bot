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
description = soup.find('h3', id="kp-wp-tab-cont-overview")

# result = html.unescape(re.findall(r"\[.*\]", res.text).pop())
# result_json = json.loads(result)

print(description)