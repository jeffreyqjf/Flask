# 使用教程
```
$ 克隆本仓库
git clone https://github.com/Clark-zy/Flask.git
```


----
配置mysql服务器使用下面命令创建表单

```
CREATE TABLE user(
  id INT(11) NOT NULL AUTO_INCREMENT,
  username VARCHAR(255) NOT NULL,
    password_hash varchar(255),
  email VARCHAR(255) NOT NULL,
  PRIMARY KEY (id)
);

```

 在.my_app文件夹中找到_init_.py,填入自己的发信服务器以及数据库信息


| config|example|usage|
| ------------- | ----------------------- | ---------------------- |
| mysqlhost| app.config['mysqlhost']='######' | 数据库ip|
| mysqluser| app.config['mysqluser']='######'| 数据库账号|
| mysqlpassword |app.config['mysqlpassword']='######'| 数据库端口|
| mysqlport| app.config['mysqlport']=######| 数据库端口|
| mysqldb|app.config['mysqldb']='######'| 数据库表名 |
| MAIL_USERNAME | MAIL_USERNAME=1@qq.com|发信邮箱账号|
| MAIL_PASSWORD|MAIL_PASSWORD=awa|发信邮箱授权码|

安装依赖

在templates和static文件夹下创建users文件夹    






