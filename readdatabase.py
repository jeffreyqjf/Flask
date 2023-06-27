import sqlite3
data = sqlite3.connect('data.db')
cursor = data.cursor()
cursor.execute('''select * from user''')
result = cursor.fetchall()
print('----user-----')
for i in result:
    print(i)
cursor.close()
data.close()


data = sqlite3.connect('remark.db')
cursor = data.cursor()
print('____remark___')
cursor.execute("""select * from user""")
result = cursor.fetchall()
for i in result:
    print(i)
cursor.close()
data.close()
