
import requests
from bs4 import BeautifulSoup
import re
import time
#from DB import class_sqlite

base_uri = 'https://adr-stock.com/'

def uri2soup(uri):
    html = requests.get(uri)
    soup = BeautifulSoup(html.text, 'html.parser')
    return soup

def extractlink(soup):
    data = soup.select('div#stbl')
    return data

soup = uri2soup(base_uri)
print(extractlink(soup))
print(soup)