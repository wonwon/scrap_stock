from jinja2 import Environment, FileSystemLoader



#gmail template
env = Environment(loader = FileSystemLoader('./', encoding = 'utf8'))
tmp = env.get_template('./tmp/gmail_html.tmpl')


html = tmp.render({ 'mailbody': 'メール本文' })
print(html)