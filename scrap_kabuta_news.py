import requests
from bs4 import BeautifulSoup
import re
import time
from DB import class_sqlite

base_uri = 'https://kabutan.jp/'
news_uri = 'stock/news?code=3681&b=n202006060057'

def uri2soup(uri):
    html = requests.get(uri)
    soup = BeautifulSoup(html.text, 'html.parser')
    return soup

def extractlink(soup):
    stocklist = {}
    data = soup.select('div.body > a[href*="stock/?code="]')
    for d in data:
        stocklist[d.text] = d['href']
    return stocklist

uri = base_uri + news_uri

soup = uri2soup(uri)
stocklist = extractlink(soup)
print(stocklist)