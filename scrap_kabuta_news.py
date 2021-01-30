import requests
from bs4 import BeautifulSoup
import time
from Gmail import SendByGmail
from jinja2 import Environment, FileSystemLoader
import configparser

# fetch url
base_uri = 'https://kabutan.jp/'
news_uri = 'info/accessranking/2_1'

# mail config
config_ini = configparser.ConfigParser()
config_ini.read('./../../CONF/config.ini', encoding = 'utf-8')
config = {}

config['FROM'] = config_ini['GMAIL']['USER']
config['TO'] = config_ini['GMAIL']['USER']
config['PASS'] =  config_ini['GMAIL']['PASS']

def uri2soup(uri):
    html = requests.get(uri)
    soup = BeautifulSoup(html.text, 'html.parser')
    return soup

def extractlink(soup):
    data = soup.select('td.acrank_title > a')
    return data

def sendmail(data):
    #gmail template
    env = Environment(loader = FileSystemLoader('./', encoding = 'utf8'))
    tmp = env.get_template('./tmp/kabutan_news_gmail.tmpl')

    for d in data: 
        body = []
        news = uri2soup(base_uri + d['href'])
        newsbody = news.select('div.body')
        body.append({
            'title' : d.text,
            'url' : base_uri + d['href'],
            'body' : newsbody,
        })
        print(body)

        html = tmp.render({
            'articles' : body })

        mail = SendByGmail(config)
        msg = mail.make(d.text, html, 'html')
        mail.send(msg)

uri = base_uri + news_uri
soup = uri2soup(uri)
pages = extractlink(soup)
sendmail(pages)
