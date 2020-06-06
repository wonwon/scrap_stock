import smtplib

import ssl

from email.mime.text import MIMEText

from email.utils import formatdate

from jinja2 import Environment, FileSystemLoader

#mail template
env = Environment(loader = FileSystemLoader('./', encoding = 'utf8'))
tmp = env.get_template('gmail_html.tmpl')

def create_message(from_addr, to_addr, bcc_addrs, subject, body):
    msg = MIMEText(body, "html", charset)
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Bcc"] = bcc_addrs
    msg["Date"] = formatdate()
    #msg.add_header('Content-type', 'text/html')
    return msg

def send(from_addr, to_addrs, msg):
    smtpobj = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
    smtpobj.login(FROM_ADDRESS, MY_PASSWORD)
    smtpobj.sendmail(from_addr, to_addrs, msg.as_string())
    smtpobj.close()

if __name__ == "__main__":
   to_addr = TO_ADDRESS
   subject = 'finance' + str(i)
   bd = html
   msg = create_message(FROM_ADDRESS, to_addr, BCC, subject, bd)
   send(FROM_ADDRESS, to_addr, msg)
   sleep(6)
