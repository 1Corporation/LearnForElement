import json
import os

import requests
from bs4 import BeautifulSoup

BASE_URL = "http://localhost/docs/help/stdlib/element/Std/"
urls = os.listdir("/home/nginx/help/ru/stdlib/element/Std/")


def for_h3(h3):
    result = {}
    for i in h3:
        elements = []
        name = i.get_text().strip()
        current = i.next_sibling
        while current and current.name != 'hr':
            elements.append(current)
            current = current.next_sibling

        # Извлекаем текст из всех элементов
        text_parts = []
        for element in elements:
            if isinstance(element, str):  # Если это строка
                text_parts.append(element.strip())
            else:  # Если это тег
                if element.get("class") == ["language-plaintext", "highlighter-rouge"]:
                    text_parts.append(element.get_text(strip=True))
                    continue
                text_parts.append(element.get_text(strip=True).replace("Доступность: КлиентИСервер", "").replace("Доступность: Сервер", "").replace("Доступность: Клиент", ""))

        result[name.replace('\u200b','')] = ' '.join(text_parts).replace('  ', ' ')
    return result


def for_h2(h2):
    result = {}
    for i in h2:
        elements = []
        name = i.get_text().strip()
        current = i.next_sibling
        while current and current.name != 'hr':
            elements.append(current)
            current = current.next_sibling

        # Извлекаем текст из всех элементов
        text_parts = []
        for element in elements:
            if isinstance(element, str):  # Если это строка
                text_parts.append(element.strip())
            else:  # Если это тег
                if element.get("class") == ["language-plaintext", "highlighter-rouge"]:
                    text_parts.append(element.get_text(strip=True))
                    continue
                text_parts.append(element.get_text(strip=True).replace("Доступность: КлиентИСервер", "").replace("Доступность: Сервер", "").replace("Доступность: Клиент", ""))

        result[name.replace('\u200b', '')] = ' '.join(text_parts).replace('  ', ' ').strip()
    return result


def main():
    result = {}

    response = requests.get(BASE_URL )
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, features="html.parser")

    main_element = soup.find_all(class_="col col--12 markdown")[0]

    h2s = for_h2(main_element.find_all('h3'))
    h3s = for_h3(main_element.find_all('h2'))

    result.update(h2s)
    result.update(h3s)

    for i in urls:
        print(i)
        response = requests.get(BASE_URL + i)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, features="html.parser")

        try:
            main_element = soup.find_all(class_="col col--12 markdown")[0]
        except IndexError:  # V8 page не содержит этого элемента, и мне лень придумывать более лаконичное решение
            continue

        h2s = for_h2(main_element.find_all('h3'))
        h3s = for_h3(main_element.find_all('h2'))

        result.update(h2s)
        result.update(h3s)

    # Файл, куда будут записана вся документация
    with open("result.json", "w+", encoding="utf-8") as file:
        file.write(json.dumps(result, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    main()
