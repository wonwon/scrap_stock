import smtplib

import ssl

from email.mime.text import MIMEText

from email.utils import formatdate

class SendByGmail:
    def __init__(self, config):
        self.__fromadd = config['FROM']
        self.__toadd = config['TO']
        self.__pass = config['PASS']
        self.__charset = 'utf-8'

    def send(self, msg):
        smtp_obj = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout = 10)
        smtp_obj.login(self.__fromadd, self.__pass)
        smtp_obj.sendmail(self.__fromadd, self.__toadd, msg.as_string())
        smtp_obj.close()

    def creat_message(self, content):
        msg = MIMEText(content['body'], "html", self.__charset)
        #msg.add_header('Content-type', 'text/html')
        msg["Subject"] = content['body']
        msg["From"] = self.__fromadd
        msg["To"] = self.__toadd
        msg["Bcc"] = self.__tobcc
        msg["Date"] = formatdate()
        return msg
