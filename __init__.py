from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import json
import uuid
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 't_ball'
app.config['MYSQL_DB'] = 'owners'

mysql = MySQL(app)

@app.route('/table', methods=['GET'])
def index():
    cur = mysql.connection.cursor()
    cur.execute("use useee")
    cur.execute("create table test(id int)")
    mysql.connection.commit()
    cur.close()
    return 'success'


@app.route('/signup', methods=['POST'])
def signup():
    if request.headers['Content-Type'] == 'application/json':
        request_data = request.json
        email = request_data['email']
        domain = email.split("@")[-1]
        cur = mysql.connection.cursor()
        cur.execute("select * from users where email_domain like %s", [domain])
        result = cur.fetchone()
        if(result == None):
            dbname = "domain" + (str(uuid.uuid1()).replace("-", ""))
            cur.execute("insert into users(name, email, email_domain, dbname) values(%s, %s, %s, %s)", [
                        request_data['name'], request_data['email'], domain, dbname])
            create(dbname)
            return "created :"+domain
        else:
            dbname = result[4]
            insert_into_db(dbname, request_data)
        mysql.connection.commit()
        cur.close()
        return "Success"

def insert_into_db(dbname, request_data):
    cur = mysql.connection.cursor()
    cur.execute("use "+dbname)
    cur.execute("insert into users(name, email ) values(%s, %s)", [
        request_data['name'], request_data['email']])
    mysql.connection.commit()
    cur.close()


def create(dbname):
    cur = mysql.connection.cursor()
    dbname_query = "create database "+dbname
    cur.execute(dbname_query)
    mysql.connection.commit()
    cur.close()
    print("Gonna create table"+dbname)
    create_user_table(dbname)
    return "Success"

def create_user_table(dbname):
    print("create table")
    cur = mysql.connection.cursor()
    create_table_query = """CREATE TABLE `users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(200) NULL,
  `email` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC))"""
    cur.execute("use "+dbname)
    cur.execute(create_table_query)
    mysql.connection.commit()
    cur.close()
    return "Success"

if __name__ == '__main__':
    app.run()
