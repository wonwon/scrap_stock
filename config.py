import configparser

config_ini = configparser.ConfigParser()
config_ini.read('./CONF/config.ini', encoding = 'utf-8')

#mail config
config = {}

config['FROM'] = config_ini['GMAIL']['USER']
config['TO'] = config_ini['GMAIL']['USER']
config['PASS'] =  config_ini['GMAIL']['USER']['PASS']