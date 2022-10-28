import datetime
from collections import namedtuple

import bs4
import requests
import re

InnerBlock = namedtuple('Block', 'title,price,currency,date,url')


class Block(InnerBlock):

    def __str__(self):
        return f'{self.title}\t{self.price} {self.currency}\t{self.date}\t{self.url}'


class OLXParser:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15',
            'Accept-Language': 'ru',
        }

    def get_page(self, page: int = None):
        params = {
            'search[filter_enum_model][0]': 'x5',
        }
        if page and page > 1:
            params['page'] = page
        url = 'https://www.olx.ua/d/uk/transport/legkovye-avtomobili/bmw/'
        r = self.session.get(url, params=params)
        return r.text

    @staticmethod
    def parse_date(item: str):
        params = item.split(' - ')
        if len(params) != 2:
            return
        params = params[1].split(' ')
        if len(params) == 3:
            day, _, time = params
            if day == 'Сьогодні':
                date = datetime.date.today()
            elif day == 'Вчора':
                date = datetime.date.today() - datetime.timedelta(days=1)
            else:
                print('Couldn\'t make out the day:', item)
                return

            time = datetime.datetime.strptime(time, '%H:%M').time()
            return datetime.datetime.combine(date=date, time=time)

        elif len(params) == 4:
            day, month_hru, year, _ = params
            months_map = {
                'січня': 1,
                'лютого': 2,
                'березня': 3,
                'квітня': 4,
                'травня': 5,
                'червня': 6,
                'липня': 7,
                'серпня': 8,
                'вересня': 9,
                'жовтня': 10,
                'листопада': 11,
                'грудня': 12,
            }
            day = int(day)
            month = months_map[month_hru]
            year = int(year)
            return datetime.datetime(day=day, month=month, year=year)

        else:
            print('Couldn\'t make out the day:', item)
            return

    def parse_block(self, item):
        # Select block with link
        url_block = item.select_one('a.css-1bbgabe')
        href = url_block.get('href')
        if href:
            url = 'https://www.olx.ua/' + href
        else:
            url = None

        # Select block with name
        title_block = item.select_one('h6.css-1pvd0aj-Text.eu5v0x0')
        title = title_block.string.strip()

        # Select block with name and currency
        price_block = item.select_one('p.css-1q7gvpp-Text.eu5v0x0')
        price_block = price_block.get_text('\n').strip()
        price_block = price_block.split('\n')[0]
        price_block = re.split(r'(?<=\d)\s(?=[а-я])', price_block)
        if len(price_block) == 2:
            price, currency = price_block
        else:
            price, currency = None, None
            print('Something went wrong while searching for a price:', price_block)

        # Select a block with the date of placement of the ad
        date = None
        date_block = item.select_one('p.css-p6wsjo-Text.eu5v0x0')
        date_block = date_block.get_text().strip()
        if date_block:
            date = self.parse_date(item=date_block)

        return Block(
            url=url,
            title=title,
            price=price,
            currency=currency,
            date=date
        )

    def get_pagination_limit(self):
        text = self.get_page()
        soup = bs4.BeautifulSoup(text, 'lxml')

        container = soup.select('.pagination-list .pagination-item a')
        last_button = container[-1]
        last_page = last_button.string.strip()
        return int(last_page)

    def get_blocks(self, page: int = None):
        text = self.get_page(page=page)
        soup = bs4.BeautifulSoup(text, 'lxml')

        # A request for a CSS selector consisting of multiple classes is made via select
        container = soup.select('[data-cy="l-card"]')
        for item in container:
            block = self.parse_block(item=item)
            print(block)

    def parse_all(self):
        limit = self.get_pagination_limit()
        print(f'Total Pages: {limit}')

        for i in range(1, limit + 1):
            self.get_blocks(page=i)


def main():
    p = OLXParser()
    p.parse_all()


if __name__ == '__main__':
    main()
