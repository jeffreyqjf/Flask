import random
import sqlite3

from my_app import app
from flask import session, redirect, render_template, url_for, request
from my_app.dbfunction import check_password, check_all_user, check_email, check_username, append_user, tokens_user
from my_app.dbfunction import change_user, tokens_user,get_token,create_user_file, check_email_whether_unique
from my_app.dbfunction import insert_into_post_table, count_post_num, insert_remark, create_remark_area_table, find_table_name
from flask import g,flash,get_flashed_messages
from my_app.email import send_password_reset_email, send_register_mail


@app.before_request
def before_request():
    g.db = sqlite3.connect(app.config['database'])
    g.remark_db = sqlite3.connect(app.config['remark_db'])
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


"""
post用于呈现用户的评论帖子 每一行是一个超链接，可以到每一个帖子里
每页有着一定的remarks，排序从点赞量高到低，每个用户点赞一次，一样的话按照排序从新到旧
点进帖子后也是一个多页的界面，分多个评论区
一个帖子对应一个发帖人，发帖的id，评论者，评论语言
数据库通过发帖人和id来确定数据库的表，一个帖子表的格式是：发帖人_id
有一个remark表储存各个帖子的基本信息 基本信息包括：发帖人，标题（限制字数），帖子id

帖子在用户自己的网站里发出
"""


@app.route('/remark/<page_number>')
def remark(page_number):
    """
    该页是说有发布的帖子
    :param page_number:
    :return:
    """
    if 'username' in session:
        username = session.get('username')
        dictionary = {}
        count = 5  # 每页的超链接个数
        if request.method == 'GET':
            cur = g.remark_db.cursor()
            cur.execute("select * from post")
            result = cur.fetchall()
            if result:  # 防止None
                dictionary['post_content'] = result[page_number * count - count, page_number * count]
            else:
                dictionary['post_content'] = []
            cur.close()
            return render_template(f'remark_post/post_page_{page_number}.html', username=username, dictionary=dictionary)
    else:
        return redirect(url_for('login'))


@app.route("/remark_area/<id>/<int:page_number>")
def remark_area(id, page_number):
    """

    :param id:
    :param page_number:
    :return:
    """
    if 'username' in session:
        username = session.get('username')
        dictionary = {}
        table_name = find_table_name(g, id)
        cur = g.remark_db.cursor()
        cur.execute(f"select * from {table_name}")
        result = cur.fetchall()
        count = 5  # 每页的评论个数
        if result:  # 防止None
            dictionary['remark'] = result[page_number * count - count, page_number * count]
        else:
            dictionary['remark'] = []
        cur.close()
        if request.method == 'GET':
            if page_number == 1:
                return render_template(f'remark_post/remark_page_main.html', username=username, dictionary=dictionary)
            else:
                return render_template(f'remark_post/remark_page_other.html', username=username, dictionary=dictionary)
        elif request.method == 'POST':
            # 发表评论
            # 获取基本信息
            remark_people = request.form.get("remark_people")
            remark = request.form.get("remark")
            table_name = find_table_name(g, id)
            insert_remark(g, table_name, remark_people, remark)
            flag = True  # 成功
            return render_template(f'remark_post/remark_page_main.html', username=username, dictionary=dictionary, flag=flag)
    else:
        return redirect(url_for('login'))


@app.route('/post', methods=['get', 'post'])
def post():
    if 'username' in session:
        username = session.get('username')
        dictionary = {}
        dictionary['username'] = username
        if request.method == 'GET':
            return render_template('remark_post/post.html', dictionary=dictionary)
        elif request.method == "POST":
            # 发布帖子
            # 获取基本信息
            title = request.form.get("title")
            main_contain = request.form.get("main_contain")
            id = count_post_num(g)  # 新的id
            herf = url_for("remark_area", id=id, page_number=1)  # 传入参数
            table_name = username + "_" + str(id)
            insert_into_post_table(g, poster_name=username, title=title, main_contain=main_contain, herf=herf)
            create_remark_area_table(g, table_name)
            return render_template("remark_post/post.html")
    else:
        return redirect(url_for('login'))

