from flask import Flask
from flask_mail import Mail

app = Flask(__name__)
app.config['database'] = 'data.db'
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = '3172268428@qq.com'
app.config['MAIL_PASSWORD'] = 'byxubvgykznvddef'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.secret_key = 'hard to guess'
mail = Mail(app)

from my_app import urls