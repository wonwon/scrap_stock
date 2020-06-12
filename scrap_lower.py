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
    body_text = []
    #stock price
    price = soup.select('span.kabuka')
    sp = re.match('([0-9,]+)', price[0].text).group(1).replace(',', '')
    if int(sp) < 500:
        #stock name category
        cp = soup.select('h2')
        ind = soup.select('#stockinfo_i2 > div')
        # stock overview
        sti = soup.select('#stockinfo_i3')[0].text.replace('\n', '')
        # stock history
        tbhead = soup.select('table.stock_kabuka0 > thead > tr')[0].text.replace('\n', ' ')
        tbl1 = soup.select('table.stock_kabuka0 > tbody > tr')[0].text.replace('\n', ' ')
        body_text.append(\
            cp[0].text + '(' + ind[0].text.replace('\n', '') + ')' + '\n'\
            + sti + '\n'\
            + tbhead + '\n'\
            + tbl1 + '\n')
        # stock history table row
        for i in range(5):
            tbl2 = soup.select('table.stock_kabuka1 > tbody > tr:nth-child(-n+5)')[i].text.replace('\n', ' ')
            body_text.append(tbl2 + '\n')

    return body_text

for i in range(1, 11):
    uri = base_uri + cont_uri + page_uri + str(i)
    stock = extlink(uri)
    for j in stock:
        print(extstock(kabutan_uri + j))
        time.sleep(1)
    time.sleep(1)

#html = tmp.render({\
#        'mailbody': stocklist['body'],\
#         })
#print(html)