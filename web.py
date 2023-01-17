from flask import Flask, render_template, \
  request, redirect, url_for

import pymysql.cursors, os

conn = cursor = None
application = Flask(__name__)

def openDb():
   global conn, cursor
   conn = pymysql.connect("localhost","root","","db_penjualan" )
   cursor = conn.cursor()	

@application.route('/')
def index():
    openDb
    container = []
    sql = "SELECT * FROM barang"
    cursor.execute(sql)
    results = cursor.fetchall()
    for data in results:
      container.append(data)
    closeDb() 
    return render_template('index.html',container=container)


if __name__ == '__main__':
   application.run(debug=True)