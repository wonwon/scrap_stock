import requests
from bs4 import BeautifulSoup
import time
import Gmail
from jinja2 import Environment, FileSystemLoader
#import re
#from DB import class_sqlite

# fetch url
#base_uri = 'https://kabutan.jp/'
#news_uri = 'stock/news?code=3681&b=n202006060057'
base_uri = 'https://selection.kabutan.jp/category/%E6%A8%AA%E5%B1%B1%E5%88%A9%E9%A6%99/'

#gmail template
env = Environment(loader = FileSystemLoader('./', encoding = 'utf8'))
tmp = env.get_template('./tmp/gmail_html.tmpl')

def uri2soup(uri):
    html = requests.get(uri)
    soup = BeautifulSoup(html.text, 'html.parser')
    return soup

def extractlink(soup):
    stocklist = {}

    data = soup.select('ol > li > div > a[href*="selection"]')
    for d in data:
        stocklist[d.text] = d['href']
    return stocklist

soup = uri2soup(base_uri)
stocklist = extractlink(soup)

print(stocklist)
#
#html = tmp.render({\
#        'mailbody': stocklist['body'],\
#            })
#
#print(html)