import sqlite3
db = sqlite3.connect('data.db')
cursor = db.cursor()
try:
    cursor.execute('''create table user(
                id integer primary key  AUTOINCREMENT,
                username varchar(20),
                password_hash varchar(800),
                email varchar(50))''')  # int(20) 和integer区别
    db.commit()
    print('成功创建用户数据表')
except:
    print('创建失败，用户数据表已创建')
cursor.close()
db.close()
remark_db = sqlite3.connect('remark.db')
cursor = remark_db.cursor()
try:
    cursor.execute('''create table post(
                    id integer primary key  AUTOINCREMENT,
                    poster_name varchar(20),
                    title varchar(20),
                    main_contain varchar(800),
                    post_id integer,
                    herf varchar(500))''')
    remark_db.commit()
    print('创建评论数据表成功')
except:
    print('创建失败，评论数据表已创建')
cursor.close()
remark_db.close()
#  poster_id 表


