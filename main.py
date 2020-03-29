import hashlib
import json
import requests
from tqdm import tqdm


class WikiLink:

    def __init__(self, file, url_link=None, country=None):
        self.file = open(file, encoding='utf-8')
        self.data = json.loads(self.file.read())
        self.session = requests.Session()
        self.country_list = list()
        self.country = country
        for item in self.data:
            for key, value in item.items():
                if key == 'name':
                    for key, value in item['name'].items():
                        if key == 'common':
                            self.country_list.append(value)
        print(f'Общее количество стран - {len(self.country_list)}, запускаем класс Итераций:')
        self.idx = 0
        self.url_link = url_link

    def __iter__(self):
        return self

    def __next__(self):
        URL = "https://en.wikipedia.org/w/api.php"
        try:
            self.country = self.country_list[self.idx]
            PARAMS = {
                "action": "query",
                "format": "json",
                "prop": "info",
                "generator": "allpages",
                "inprop": "url",
                "gapfrom": self.country,
                "gaplimit": 1
            }
            response = self.session.get(url=URL, params=PARAMS).json()
            response = response["query"]["pages"]
            for item in response.values():
                for key, value in item.items():
                    if key == "fullurl":
                        self.url_link = value
            self.idx += 1
        except requests.ConnectionError as er:
            self.url_link = str(er)
        except IndexError:
            raise StopIteration
        return {self.country: self.url_link}


def md5_get(file):
    list_of_md5_lines = list()
    with open(file) as treated_file:
        data = json.loads(treated_file.read())
        print(f'Общее количество строк - {len(data)}, запускаем функцию Генерации:')
        print('Выводим список md5 hash:')
        for i, line in enumerate(data):
            line_md5 = hashlib.md5(str.encode(str(line)))
            list_of_md5_lines.append(line_md5)
            yield line, line_md5
    return print(f'Общее количество: {len(list_of_md5_lines)}')


if __name__ == '__main__':
    list_of_counties_and_url_links = list()
    for url_link in tqdm(WikiLink("countries.json")):
        list_of_counties_and_url_links.append(url_link)
    print('Ссылки сформированы, начинаем запись файла:')
    with open("countries_url_link.json", 'w') as file_countries_url_link:
        file_countries_url_link.write(json.dumps(list_of_counties_and_url_links, ensure_ascii=False))
    print('Файл записан!\n')

    for md5_line in md5_get("countries_url_link.json"):
        print(md5_line)
