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
except:
    print('用户数据库已创建')
remark_db = sqlite3.connect('remark.db')
cursor = remark_db.cursor()
try:
    pass
except:
    pass
cursor.close()
remark_db.close()
