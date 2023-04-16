import json
import re

import json
from multiprocessing import Pool
from bs4 import BeautifulSoup
import requests


class Quke:
    def __init__(self):
        self.data = {}
        self.up_data()

    def get_prod(self, args):
        type, n_page, type_r = args

        url = 'https://quke.ru/shop/komplektuushie-dlya-pk/' + type
        r = requests.get(f'{url}?page={n_page}')
        soup = BeautifulSoup(r.text, "html.parser")

        cards = soup.find_all('div', class_='b-card2-v2__inner')

        data = []
        for n, i in enumerate(cards):
            try:
                name_a = i.find('a', class_='b-card2-v2__name')
                link_prod = name_a['href']
                name = name_a.text
                price = i.find('div', class_='b-card2-v2__price').text
                price = price.split('\n')[2]
                price = int(price.replace(' ', ''))

                img = i.find('img', class_='lazyload')
                img_link = img['src']

                data.append({
                    'name'    : name,
                    'price'   : price,
                    'link'    : 'https://quke.ru' + link_prod,
                    'img_link': 'https://quke.ru' + img_link,
                    'type'    : type_r
                })
            except Exception as e:
                print(f"{n_page} ::: {n} -- {e}")
        return data

    def get_all_prod(self, type='processory', type_r='processor'):
        url = 'https://quke.ru/shop/komplektuushie-dlya-pk/' + type
        # sesia = requests.session()
        # headers = {'x-requested-with': 'XMLHttpRequest',
        #            'user-agent'      : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 YaBrowser/19.10.3.281 Yowser/2.5 Safari/537.36'}
        #
        # r = sesia.get(url, headers=headers, timeout=5)
        # soup = BeautifulSoup(r.content, "html.parser")
        #
        # print(r.content)

        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        count_page = int(list(soup.find_all('li', class_='pagination2__item'))[-2].text)
        with Pool(count_page) as p:
            data = []
            for i in p.map(self.get_prod, [[type, i + 1, type_r] for i in range(count_page)]):
                data += i
        # print(json.dumps(data, ensure_ascii=False, indent=4))
        return data

    def up_data(self):
        types = {
            'card'       : 'videokarty',
            'processor'  : 'processory',
            'motherboard': 'materinskie-platy',
            'RAM'        : 'operativnaya-pamyat',
            'power'      : 'bloki-pitaniya-dlya-komputerov',
            'memory'     : 'vnutrennie-jestkie-diski-hdd-ssd-i-sshd',
        }
        # types = ['videokarty', 'processory', 'materinskie-platy', 'operativnaya-pamyat', 'bloki-pitaniya-dlya-komputerov', 'vnutrennie-jestkie-diski-hdd-ssd-i-sshd']
        self.data = []
        for type in types:
            self.data.extend(self.get_all_prod(types[type], type))

    def safe(self):
        json.dump(self.data, open('quke.ru.json', 'w', encoding='utf8'), ensure_ascii=False, indent=4)


def main():
    quke1 = Quke()
    quke1.safe()


if __name__ == '__main__':
    main()