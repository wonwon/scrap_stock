import requests
from bs4 import BeautifulSoup
import time
from Gmail import SendByGmail
from jinja2 import Environment, FileSystemLoader
import re
import urllib.parse
import configparser
# mail config
config_ini = configparser.ConfigParser()
config_ini.read('./../../CONF/config.ini', encoding = 'utf-8')
config = {}

config['FROM'] = config_ini['GMAIL']['USER']
config['TO'] = config_ini['GMAIL']['USER']
config['PASS'] =  config_ini['GMAIL']['PASS']


#uri
# kabutan theme url
base_uri = 'https://kabutan.jp'
stock_uri = '/stock/kabuka?code='
page_uri = '&market=0&capitalization=-1&stc=zenhiritsu&stm=1&page='
yahoo_uri = 'https://stocks.finance.yahoo.co.jp/stocks/history/?code='
# kabureal uri
kabureal = 'http://kabureal.net/brand/?code='


def uri2soup(uri):
    #uri to soup object
    html = requests.get(uri)
    soup = BeautifulSoup(html.text, 'html.parser')
    return soup

def extlink(uri):
    # extract link from themes page
    soup = uri2soup(uri)
    data = soup.select('td.td29 > a')
    return data

def extstockuri(uri):
    # extract code and close stock from list
    soup = uri2soup(uri)
    data = {}
    links = soup.select('td.tac > a')
    stocks = soup.select('table.stock_table > tr > td:nth-child(6)')
    for i in range(len(links)):
        if stocks[i].text == '－':
            data[links[i].text] = '600'
        else:
            data[links[i].text] = stocks[i].text

    return data

def extimg(uri):
    #extract chart img from code
    soup = uri2soup(uri)
    return soup.select('div.tcenter > img')[0]['src']

def extstock(uri):
    # extract stock data from kabutan
    soup = uri2soup(uri)
    #stock name category
    body = {}
    body['name'] = soup.select('h1')[0].text
    body['stock'] = soup.select('td.stoksPrice')[1].text
    body['industory'] = soup.select('dd.category')[0].text
    #print(soup.select('table.boardFin > tr:nth-child(-n+6)'))#:nth-child(-n+6)'))
    # stock history table row
    #for i in range(6):
        #body['past' + str(i)] = soup.select('table.boardFin > tbody > tr:nth-child(-n+6)')[i].text.replace('\n', ' ')
         
    return body

def sendmail(title, uri):
    #gmail template
    env = Environment(loader = FileSystemLoader('./', encoding = 'utf8'))
    tmp = env.get_template('./tmp/gmail_html.tmpl')
    body = []
    for i in range(1, 5):
        time.sleep(5)
        links = extlink(uri + str(i))
        for j in range(len(links)):
            time.sleep(2)
            grep = re.match(r'.*?(\d+)\..$', links[j]['href'])
            stock = str(grep.group(1))
            print(stock)
            #extract kabureal img
            img = extimg(kabureal + stock)
            info = extstock(links[j]['href'])
            body.append({
                'name' : info['name'],
                'code' : stock,
                'stock' : info['stock'],
                'img' : img,
                'url' : links[j]['href'],
                'info' : info['industory'],
            })

    html = tmp.render({
        'theme' : title ,
        'articles' : body })
    mail = SendByGmail(config)
    msg = mail.make(title, html, 'html')
    mail.send(msg)

uri = {
    '連騰株' : 'http://kabureal.net/continueup/?page=',\
    '短期急騰株' : 'http://kabureal.net/raterank/span/?d=1&page=',\
}

for k, v in uri.items():
    print(k + ' ' + v)
    sendmail(k , v)