""" WIP """
import requests
from bs4 import BeautifulSoup

parsed_html = BeautifulSoup(
    requests.get('https://en.wikipedia.org/wiki/Republican_Party_presidential_primaries,_2016').content.decode(),
    'html.parser'
)
all_tables = parsed_html.body.findAll('table', class_='wikitable')
import ipdb; ipdb.set_trace()
schedule_table = [table for table in all_tables if 'Date' in str(table.find('th'))][0]
i = 0
