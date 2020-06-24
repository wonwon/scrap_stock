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
    data = {}
    data['link'] = soup.select('div.mtop5 > a')
    data['exchange'] = soup.select('div.mtop3')
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
    body = {}
    #stock name category
    body['name'] = soup.select('h2')[0].text
    body['stock'] = soup.select('span.kabuka')[0].text
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

def sendmail(uri):
    #gmail template
    env = Environment(loader = FileSystemLoader('./', encoding = 'utf8'))
    tmp = env.get_template('./tmp/gmail_html.tmpl')
    body = []
    for i in range(1, 7):
        time.sleep(5)
        links = extlink(uri + str(i))
        ex = links['exchange']
        for j in range(len(ex)):
            print(type(ex[j].text))
            print(type("福"))
            if "福" in ex[j].text:# or '福' in ex[j].text:
                print(ex[j].text)
            else:
                #print(ex[j].text.decode('utf-8'))
                time.sleep(2)
                grep = re.match(r'.*?(\d+)$', links['link'][j]['href'])
                #extract kabureal img
                img = extimg(kabureal + str(grep.group(1)))
                inf = extstock(base_uri + stock_uri + str(grep.group(1)))
                body.append({
                    'name' : inf['name'],
                    'code' : str(grep.group(1)),
                    'stock' : inf['stock'],
                    'img' : img,
                    'info' : inf['info'],
                    'head' : inf['tbhead'],
                    'table' : inf['past'],
                })
                print(body)

        html = tmp.render({
            'theme' : 'continueup' + str(i),
            'articles' : body })
        mail = SendByGmail(config)
        msg = mail.make('continueup' + str(i), html, 'html')
        mail.send(msg)

uri = 'http://kabureal.net/continueup/?page='
sendmail(uri)