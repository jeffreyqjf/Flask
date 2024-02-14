import threading
from my_app import app, mail
from flask_mail import Message
from flask import render_template
import os


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    thr = threading.Thread(target=send_async_email, args=[app, msg])
    thr.start()
def send_register_mail(recipients, username,token):
    #print(recipients, username,token)
    print(render_template('email/register_mail.txt', user=username, token=token))
    #print(render_template('email/register_mail.html', user=username, token=token))

    send_mail('口令验证',
              sender=app.config['MAIL_USERNAME'],
              recipients=[recipients],
              text_body=render_template('email/register_mail.txt', user=username, token=token),
              html_body=render_template('email/register_mail.html', user=username, token=token)
              )

def send_password_reset_email(token, recipients, username):

    send_mail('重置密码',
              sender=app.config['MAIL_USERNAME'],
              recipients=[recipients],
              text_body=render_template('email/reset_password.txt', user=username, token=token),
              html_body=render_template('email/reset_password.html', user=username, token=token)
              )
