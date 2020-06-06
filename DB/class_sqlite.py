import sys
import sqlite3

class Database:
    def __init__(self, name):
       self._conn = sqlite3.connect(name)
       self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchnone(self):
        return self.cursor.fetchnone()

    def query(self, sql, params = None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

#with Database('db_kabutan_stock.sqlite') as db:
    #db.execute('CREATE TABLE company_info(id INTEGER PRIMARY KEY AUTOINCREMENT, code INTEGER, name varchar(50), industry varchar(50))')
    #db.execute('CREATE TABLE stock_info(id INTEGER PRIMARY KEY AUTOINCREMENT, code INTEGER, date varchar(20), open integer, close integer, hight integer, low integer, volume integer)')
    #db.execute('CREATE TABLE credit_info(id INTEGER PRIMARY KEY AUTOINCREMENT, code INTEGER, date varchar(50), marginbuy integer, marginsale iteger, ratio integer)')

#with Database('db_file.sqlite') as db:
#   db.execute('CREATE TABLE compayt_info(id INTEGER PRIMARY KEY AUTOINCREMENT, code INTEGER, name TEXT, cat TEXT)')
#
#with Database('my_db.sqlite') as db:
#    db.execute('CREATE TABLE comments(pkey INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR, comment_body VARCHAR, date_posted TIMESTAMP)')
#    db.execute('INSERT INTO comments (username, comment_body, date_posted) VALUES (?, ?, current_date)', ('tom', 'this is a comment'))
#    comments = db.query('SELECT * FROM comments')
#    print(comments)
