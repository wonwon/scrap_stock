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
rank_uri = '/info/accessranking/3_2'
theme_uri = '/themes/?theme='
stock_uri = '/stock/kabuka?code='
page_uri = '&market=0&capitalization=-1&stc=zenhiritsu&stm=1&page='
# kabureal uri
kabureal = 'http://kabureal.net/brand/?code='


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
        if stocks[i].text == '－':
            data[links[i].text] = '600'
        else:
            data[links[i].text] = stocks[i].text

    return data

def extkaburealdata(uri):
    soup = uri2soup(uri)
    return soup.select('div.tcenter > img')[0]['src']

def extstock(uri):
    soup = uri2soup(uri)
    body = {}
    #stock name category
    body['name'] = soup.select('h2')[0].text
    body['industory'] = soup.select('#stockinfo_i2 > div > a')[0].text.replace('\n', '')
    # stock overview
    body['info'] = soup.select('#stockinfo_i3 > table > tbody > tr:first-child')[0].text.replace('\n', '')
    # stock history
    body['tbhead'] = soup.select('table.stock_kabuka0 > thead > tr')[0].text.replace('\n', ' ')
    body['past'] = soup.select('table.stock_kabuka0 > tbody > tr')[0].text.replace('\n', ' ')
    # stock history table row
    for i in range(5):
        body['past' + str(i)] = soup.select('table.stock_kabuka1 > tbody > tr:nth-child(-n+5)')[i].text.replace('\n', ' ')
         
    return body

#gmail template
env = Environment(loader = FileSystemLoader('./', encoding = 'utf8'))
tmp = env.get_template('./tmp/gmail_html.tmpl')

# extract themelink
links = extlink(base_uri +  rank_uri)
for i in range(5):
    body = []
    # extract stock link & price links[i].text
    for j in range(1, 5):
        list_uri = base_uri + theme_uri + urllib.parse.quote(links[i].text) + page_uri + str(j)
        data = extstockuri(list_uri)
        for code, stock in data.items():
            #extract under 600 yen
            if int(re.sub('\D', '', stock)) < 600:
                time.sleep(2)
                #extract kabureal img
                img = extkaburealdata(kabureal + str(code))
                inf = extstock(base_uri + stock_uri + str(code))
                print(inf['name'])
                body.append({
                    'name' : inf['name'],
                    'code' : str(code),
                    'stock' : str(stock),
                    'img' : img,
                    'info' : inf['info'],
                    'head' : inf['tbhead'],
                    'table' : inf['past'],
                })

    print(links[i].text)
    html = tmp.render({
        'theme' : links[i].text,
        'articles' : body })
    print(html)
    mail = SendByGmail(config)
    msg = mail.make(links[i].text, html, 'html')
    mail.send(msg)

