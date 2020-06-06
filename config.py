import configparser

config_ini = configparser.ConfigParser()
config_ini.read('./../../CONF/config.ini', encoding = 'utf-8')

#mail
fromadd = config_ini['DEFAULT']['User']
print(fromadd)
passwd =  config_ini['DEFAULT']['Pass']
toadd = config_ini['DEFAULT']['To']
bcc = ""
charset = 'utf-8'