import random
import sqlite3

from my_app import app
from flask import session, redirect, render_template, url_for, request
from my_app.dbfunction import check_password, check_all_user, check_email, check_username, append_user, tokens_user
from my_app.dbfunction import change_user, tokens_user,get_token,create_user_file, check_email_whether_unique
from flask import g,flash,get_flashed_messages
from my_app.email import send_password_reset_email, send_register_mail



@app.before_request
def before_request():
    g.db = sqlite3.connect(app.config['database'])

    if session.get('token_register'):
        g.token_register = session.get('token_register')
        g.email_save = session.get('email_save')
        g.password_save = session.get('password_save')
        g.username_save = session.get('username_save')




@app.teardown_request
def teardown_request(e):
    db = getattr(g, 'db', None)
    if db:
        db.close()
    g.db.close()


@app.route('/')
def home():
    return redirect(url_for('index'))


@app.route('/index', methods=['get'])
def index():
    if 'username' in session:
        username = session.get('username')

        return render_template('index.html', username=username)
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['get', 'post'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            print(username)
            print(password)
            if not (username or password):
                error = '请填写有效信息'
                return render_template('login.html', error=error)
            else:
                if check_password(g, username, password):
                    session['username'] = username
                    return redirect(url_for('index'))
                else:
                    error = '账号密码错误'
                    return render_template('login.html', error=error)
        else:
            return render_template('login.html')


@app.route('/logout', methods=['get', 'post'])
def logout():
    if 'username' in session:
        username = session.get('username')
        if request.method == 'GET':
            return render_template('logout.html')
        else:
            session.pop('username', None)

            return redirect(url_for('login'))
    return redirect(url_for('login'))


@app.route('/register', methods=['get', 'post'])
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        password_again = request.form.get('password_again')
        username = request.form.get('username')
        if not (email and password_again and password and username):
            error = '请填写完整信息'
            return render_template('register.html', error=error)
        elif password != password_again:
            error = '两次密码不一致'
            return render_template('register.html', error=error)
        elif check_username(g, username):
            error = '用户名已存在'
            return render_template('register.html', error=error)
        elif not check_email_whether_unique(g, email):
            error = '邮箱已注册'
            return render_template('register.html', error=error)
        else:
            token = random.randint(1000, 9999)  # 发送动态口令
            send_register_mail(email, username=username, token=token)
            session['token_register'] = str(token)
            session['email_save'] = email
            session['password_save'] = password
            session['username_save'] = username
            return redirect(url_for('register_token'))


@app.route('/register_token', methods=['get', 'post'])
def register_token():
    if request.method == "GET":
        if not g.get('token_register'):
            return render_template('404.html')
        else:

            error = get_flashed_messages()
            if error:
                error = error[0]

            return render_template('register_token.html',error=error)
    else:
        token_register = session.get('token_register')
        token_register_check = request.form.get('token_register_check')
        # check register token
        if token_register_check == token_register:
            password = session.get('password_save')
            email = session.get('email_save')
            username = session.get('username_save')
            create_user_file(username)
            append_user(g, username, password, email)
            return render_template('register_successful.html')
        else:
            flash('验证码错误')
            return redirect(url_for('register_token'))


@app.route('/all_user')
def all_user():
    user = check_all_user(g)
    return render_template('all_user.html', user=user)


@app.route('/reset_password_request',methods=['get','post'])
def reset_password_request():
    if request.method == 'GET':
        return render_template('reset_password_request.html')
    else:
        email = request.form.get('email')
        username = request.form.get('username')
        if not check_email(g, email, username):
            print(check_email(g, email, username))
            error = '无该用户'
            return render_template('reset_password_request.html',error=error)
        else:
            print('reset_password_request email:',email)
            values = get_token(g,email=email)
            send_password_reset_email(token=values[0],recipients=values[1],username=values[2])
            return render_template('reset_password_request_successful.html')


@app.route('/reset_password/<token>', methods=['get', 'post'])
def reset_password(token):
    if request.method == 'GET':
        if not tokens_user(g, token):
            return render_template('404.html')
        else:
            username = tokens_user(g,token)[1]
            return render_template('reset_password.html',token=token)
    else:
        if not tokens_user(g, token):
            return render_template('404.html')
        else:
            username = tokens_user(g,token)[1]
            set_password = request.form.get('set_password')
            set_password_again = request.form.get('set_password_again')
            if set_password_again != set_password:
                error = '密码不一致'
                return render_template('reset_password.html', error=error)
            else:
                change_user(g, user=username, set_password=set_password)
                return render_template('set_password_successful.html')
@app.route("/user_page/<page_number>")
def user_page(page_number):
    if 'username' in session:
        username = session.get('username')
        return render_template(f'users/{username}/user_page_{page_number}.html', username=username)
    else:
        return redirect(url_for('login'))



