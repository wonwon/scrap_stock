import requests
from bs4 import BeautifulSoup
import time
from mail import SendByGmail
from jinja2 import Environment, FileSystemLoader
#import re
#from DB import class_sqlite

# fetch url
base_uri = 'https://kabutan.jp/'
news_uri = 'stock/news?code=3681&b=n202006060057'

#gmail template
env = Environment(loader = FileSystemLoader('./', encoding = 'utf8'))
tmp = env.get_template('./tmp/gmail_html.tmpl')

def uri2soup(uri):
    html = requests.get(uri)
    soup = BeautifulSoup(html.text, 'html.parser')
    return soup

def extractlink(soup):
    stocklist = {}
    sotcklist['title'] = soup.select('article > h1')[0]
    stocklist['body'] = soup.select('article')[0]

    data = soup.select('div.body > a[href*="stock/?code="]')
    for d in data:
        stocklist[d.text] = d['href']
    return stocklist

uri = base_uri + news_uri
soup = uri2soup(uri)
stocklist = extractlink(soup)
print(stocklist)