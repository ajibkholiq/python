#! C:\Users\user\AppData\Local\Programs\Python\Python39\python.exe
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

#fungsi koneksi database
app.config['MYSQL_HOST'] = 'ajibkholiq.com'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_penjualan'
mysql = MySQL(app)

def cursor():
   global cur
   cur=mysql.connection.cursor()
def commit():      
   return mysql.connection.commit()
#fungsi view index() untuk menampilkan data dari database
@app.route('/')
def index():   
   cursor()
   container = []
   sql = "SELECT * FROM barang"
   cur.execute(sql)
   results = cur.fetchall()
   for data in results:
      container.append(data)
   cur.close()
   return render_template('index.html', container=container,)

#fungsi view tambah() untuk membuat form tambah
@app.route('/tambah', methods=['GET','POST'])
def tambah():
   if request.method == 'POST':
      cursor()
      nama = request.form['nama']
      harga = request.form['harga']
      stok = request.form['stok']
      sql = "INSERT INTO barang (nama_barang, harga,stok) VALUES (%s, %s, %s)"
      val = (nama, harga, stok)
      cur.execute(sql, val)
      commit()
      cur.close()
      return redirect(url_for('index'))
   else:
      return render_template('tambah.html')
#fungsi view edit() untuk form edit
@app.route('/edit/<id_barang>', methods=['GET','POST'])
def edit(id_barang):
   cursor()
   cur.execute('SELECT * FROM barang WHERE id_barang=%s', [id_barang])
   data = cur.fetchone()
   if request.method == 'POST':
      id_barang = request.form['id_barang']
      nama = request.form['nama']
      harga = request.form['harga']
      stok = request.form['stok']
      sql = "UPDATE barang SET nama_barang=%s, harga=%s, stok=%s WHERE id_barang=%s"
      val = (nama, harga, stok, id_barang)
      cur.execute(sql, val)
      commit()
      cur.close()
      return redirect(url_for('index'))
   else:
      return render_template('edit.html', data=data)
#fungsi untuk menghapus data
@app.route('/hapus/<id_barang>', methods=['GET','POST'])
def hapus(id_barang):
   cursor()
   cur.execute('DELETE FROM barang WHERE id_barang=%s', (id_barang,))
   commit()
   cur.close()
   return redirect(url_for('index'))
      


if __name__ == '__main__':
   app.run(debug=True)