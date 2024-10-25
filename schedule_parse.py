import datetime
import json
import requests
import fake_useragent
from bs4 import BeautifulSoup

user = fake_useragent.UserAgent().random

cookies = {
    '_ym_uid': '1720521836914747025',
    '_ym_d': '1720521836',
    'JSESSIONID': '5B049398BC1ECCCA723C1E39C8538C8C',
    '_ym_isad': '1',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    # 'cookie': '_ym_uid=1720521836914747025; _ym_d=1720521836; JSESSIONID=5B049398BC1ECCCA723C1E39C8538C8C; _ym_isad=1',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "YaBrowser";v="24.10", "Yowser";v="2.5"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': user
}
studies_time = {
    '1': '08:00-09:30',
    '2': '09:40-11:10',
    '3': '11:20-12:50',
    '4': '13:00-14:30',
    '5': '14:40-16:10',
    '6': '16:20-17:50',
    '7': '18:00-19:30',
    '8': '19:40-21:10'
}


def main():
    data = []
    today = datetime.date.today()
    # today = datetime.date.today() + datetime.timedelta(days=3)
    # print(today)
    link = f"https://www.kstu.ru/www_Ggrid.jsp?x=www_GFgrid&d={today}&f=320&g=41886#{today}"
    response = requests.get(link, headers=headers, cookies=cookies).text
    soup = BeautifulSoup(response, 'lxml')
    # print(soup)
    block = soup.find('div', class_='col-12 d-none d-md-block mygrid').find_all('tr')
    try:
        for i, bl in enumerate(block):
            if i != 0 and (bl.find('td', bgcolor='#DBFDDF').text != "   "):
                data.append({
                    'studies_time': str(studies_time[f'{i}']),
                    'Name': bl.find('td', bgcolor='#DBFDDF').text
                })
        # print(data)
        with open('day_schedule.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except AttributeError:
        data = []
        with open('day_schedule.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
