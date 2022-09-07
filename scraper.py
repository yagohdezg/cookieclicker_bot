import re
import json
import requests
from bs4 import BeautifulSoup

def scrape():
    r = requests.get('https://cookieclicker.fandom.com/wiki/Save')
    soup = BeautifulSoup(r.text, 'html.parser')
    tables = soup.find_all('table')

    cookie_dict = {}

    for table in tables:
        lines = table.find_all('tr')
        for line in lines:
            # Titles
            titles = line.find('th')
            if titles:
                col_span_attr = line.find('th').attrs.get('colspan')
                if col_span_attr:
                    title = line.getText().strip()
                    cookie_dict[title] = {}
            
            # Keys
            key = line.find('td')
            if key:
                cookie_dict[title][key.getText().strip()] = ''
            
    cookie_dict.pop('Empty', None)
    print(cookie_dict)

    cookie_dict = json.dumps(cookie_dict)
    with open('cookie_dict.txt', 'w+') as file:
        file.write(cookie_dict)