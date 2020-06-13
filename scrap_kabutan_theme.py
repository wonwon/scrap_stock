import requests
from bs4 import BeautifulSoup
import time
import Gmail
from jinja2 import Environment, FileSystemLoader
import re
import urllib.parse
#from DB import class_sqlite

#uri
# kabutan theme url
base_uri = 'https://kabutan.jp'
rank_uri = '/info/accessranking/3_2'
theme_uri = '/themes/?theme='
page_uri = '&market=0&capitalization=-1&stc=zenhiritsu&stm=1&page='


def uri2soup(uri):
    html = requests.get(uri)
    soup = BeautifulSoup(html.text, 'html.parser')
    return soup

def extlink(uri):
    soup = uri2soup(uri)
    data = soup.select('td.acrank_url > a')
    return data

def extstockuri(uri):
    soup = uri2soup(uri)
    data = {}
    links = soup.select('td.tac > a')
    stocks = soup.select('table.stock_table > tr > td:nth-child(6)')
    for i in range(len(links)):
        data[links[i].text] = stocks[i].text

    return data

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

links = extlink(base_uri +  rank_uri)
for i in range(5):
    for j in range(1, 2):
        time.sleep(2)
        list_uri = base_uri + theme_uri + urllib.parse.quote(links[i].text) + page_uri + str(j)
        data = extstockuri(list_uri)
        print(data)
        for k, v in data.items():
            print(k, v)
            if int(re.sub('\D', '', v)) < 600:
                print("Hit" + k)
            


#gmail template
env = Environment(loader = FileSystemLoader('./', encoding = 'utf8'))
tmp = env.get_template('./tmp/gmail_html.tmpl')
#html = tmp.render({\
#        'mailbody': stocklist['body'],\
#         })
#print(html)