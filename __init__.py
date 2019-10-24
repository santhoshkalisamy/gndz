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

@app.route('/delete/<user_id>', methods=['DELETE'])
def deleteUser():
    print(user_id)

@app.route('/signup', methods=['POST'])
def signup():
    if request.headers['Content-Type'] == 'application/json':
        cur = mysql.connection.cursor()
        try:
            request_data = request.json
            email = request_data['email']
            domain = email.split("@")[-1]
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
        except:
            return "Failed"
        finally:
            cur.close()
        return "Success"

def insert_into_db(dbname, request_data):
    cur = mysql.connection.cursor()
    try:
        cur.execute("use "+dbname)
        cur.execute("insert into users(name, email ) values(%s, %s)", [
        request_data['name'], request_data['email']])
        mysql.connection.commit()
    except Exception as e:
        raise e
    finally:
        cur.close()

def create(dbname):
    cur = mysql.connection.cursor()
    try:
        dbname_query = "create database "+dbname
        cur.execute(dbname_query)
        mysql.connection.commit()
        create_user_table(dbname)
    except Exception as e:
        raise e
    finally:
        cur.close()
    return "Success"

def create_user_table(dbname):
    cur = mysql.connection.cursor()
    create_table_query = """CREATE TABLE `users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(200) NULL,
  `email` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC))"""
    try:
        cur.execute("use "+dbname)
        cur.execute(create_table_query)
        mysql.connection.commit()
    except Exception as e:
        raise e
    finally:
        cur.close()
    return "Success"

if __name__ == '__main__':
    app.run()
