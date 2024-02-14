from flask import Flask
from flask_mail import Mail

app = Flask(__name__)
app.config['mysqlhost']='######'
app.config['mysqluser']='######'
app.config['mysqlpassword']='######'
app.config['mysqlport']=######
app.config['mysqldb']='######'
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = '############'
app.config['MAIL_PASSWORD'] = '############'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['SECRET_KET'] = 'hard to guess'
app.secret_key = 'hard to guess'
mail = Mail(app)

from my_app import urls
