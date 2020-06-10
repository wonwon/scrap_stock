import requests
from bs4 import BeautifulSoup
import time
import Gmail
from jinja2 import Environment, FileSystemLoader
import re
#from DB import class_sqlite

#uri
# kabu real url
base_uri = 'http://kabureal.net/'
cont_uri = 'continueup/'
page_uri = '?page='
#kabu tan url
kabutan_uri = 'https://kabutan.jp/stock/kabuka?code='

#gmail template
env = Environment(loader = FileSystemLoader('./', encoding = 'utf8'))
tmp = env.get_template('./tmp/gmail_html.tmpl')

def uri2soup(uri):
    html = requests.get(uri)
    soup = BeautifulSoup(html.text, 'html.parser')
    return soup

def extlink(uri):
    soup = uri2soup(uri)
    data = soup.select('div.mtop5 > a[href*="brand/?code="]')
    stock = []
    for d in data:
        stock.append(re.findall(r'\d{4}$', d['href'])[0])
    return stock

def extstock(uri):
    soup = uri2soup(uri)
    price = soup.select('span.kabuka')
    stockinfo = soup.select('table.stockinfo_i3')
    tbl1 = soup.select('table.stock_kabuka0')
    tbl2 = soup.select('table.stock_kabuka0')
    print(price[0].text)
    #print(stockinfo.text)
    #print(tbl1.text)
    #print(tbl2.text)

for i in range(1, 11):
    uri = base_uri + cont_uri + page_uri + str(i)
    stock = extlink(uri)
    for j in stock:
        extstock(kabutan_uri + j)
        time.sleep(1)
    time.sleep(1)

#html = tmp.render({\
#        'mailbody': stocklist['body'],\
#         })
#print(html)