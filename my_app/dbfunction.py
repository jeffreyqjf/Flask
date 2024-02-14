import jwt
from werkzeug.security import check_password_hash, generate_password_hash
from my_app import app
from flask_mail import Message
from  my_app.email import send_password_reset_email
from time import time
import os
import shutil

def check_password(g, username, password):
    cur = g.db.cursor()
    cur.execute(f'select * from user where username="{username}"')

    result = cur.fetchone()
    #print('check_password', result)
    if result:
        result = result[2]
    else:
        return False  # 出现账号密码错误，实际是没有该用户
    cur.close()
    return check_password_hash(result, password)


def check_all_user(g):
    cur = g.db.cursor()
    cur.execute(f'select * from user ')
    result = cur.fetchone()
    cur.close()
    return result


def check_username(g, username):
    cur = g.db.cursor()
    cur.execute(f'select * from user where username="{username}"')
    result = cur.fetchone()
    cur.close()
    return result


def check_email_whether_unique(g, email):
    """
    this function is used to confirm that email is not used again
    :param g: g.db is a database
    :param email: email is checked whether it is unique in user table
    :return: bool
    """
    cursor = g.db.cursor()
    cursor.execute(f'select * from user where email="{email}"')
    result = cursor.fetchone()
    if result:
        return False
    else:
        return True


def check_email(g, email, username):
    cur = g.db.cursor()
    cur.execute('select * from user where email=%s', (email,))
    result = cur.fetchone()
    cur.close()
    #print(result)
    if result is not None:
        if username in result:
            return True
        else:
            return False
    else:
        return False


def append_user(g, username, password, email):
    cur = g.db.cursor()
    password_hash = generate_password_hash(password)
    #print(password_hash,type(password_hash))
    #print("email:",email)
    #print(password,type(password))
    #print(username)
    cur.execute('insert into user(username,password_hash,email) values(%s,%s,%s)',(username,password_hash,email))
    g.db.commit()
    #print('welcome to new user')
    cur.close()

def get_token(g,email,expires_in=600):
    cur = g.db.cursor()
    cur.execute('select * from user where email=%s',(email,))
    result = cur.fetchone()
    cur.close()
    #print('result:',result)
    #print('id:',result[0])
    if result :
        token = jwt.encode({'reset_password':result[0],'exp': time() + expires_in},app.config['SECRET_KET'],algorithm='HS256')
        #print('token:',type(token),token)
        #print('username:',result[1])

        return (token,result[3],result[1])

def tokens_user(g,token):
    cur = g.db.cursor()
    user_id = jwt.decode(token,app.config['SECRET_KET'],algorithms=['HS256'])['reset_password']
    if user_id:
        cur.execute(f'select * from user where id={user_id}')
        result = cur.fetchone()
        return result
        cur.close()
    else:
        cur.close()
        #print('id is none')


def change_user(g,user,set_password):
    cur = g.db.cursor()
    cur.execute('update user set password_hash = %s where username=%s',(generate_password_hash(set_password),user))
    g.db.commit()
    cur.close()


def create_user_file(username):
    #print(os.getcwd())  # C:\Users\de'l'l\PycharmProjects\web
    path = os.path.join(os.getcwd(), 'my_app')
    if not os.path.exists(os.path.join(path, f'templates\\users\\{username}')):  # if it was not the user I care
        os.mkdir(os.path.join(path, f'templates\\users\\{username}'))  # create html
        os.mkdir(os.path.join(path, f'static\\users\\{username}'))  # create css

        shutil.copy(os.path.join(path, 'templates\\index.html'),
                    os.path.join(path, f'templates\\users\\{username}\\index.html'))
        shutil.copy(os.path.join(path, 'static\\index.css'),
                    os.path.join(path, f'static\\users\\{username}\\index.css'))  # copy index.html
        shutil.copy(os.path.join(path, 'templates\\user_page_1.html'),
                    os.path.join(path, f'templates\\users\\{username}\\user_page_1.html'))
        shutil.copy(os.path.join(path, 'static\\user_page.css'),
                    os.path.join(path, f'static\\users\\{username}\\user_page.css'))

