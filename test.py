from Gmail import SendByGmail
import configparser
# mail config
config_ini = configparser.ConfigParser()
config_ini.read('./../../CONF/config.ini', encoding = 'utf-8')
config = {}

config['FROM'] = config_ini['GMAIL']['USER']
config['TO'] = config_ini['GMAIL']['USER']
config['PASS'] =  config_ini['GMAIL']['PASS']


mail = SendByGmail(config)
print(mail.make('htm', 'html', 'html'))
a = '-'

if a.isnumeric() :
    print('ture')
else:
    print(type(a))
    print('False')