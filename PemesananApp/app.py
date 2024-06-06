from flask import Flask, jsonify, render_template, request
from flask_mysqldb import MySQL
from flask import render_template
from datetime import datetime
import requests
import json


app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'logistik'

mysql = MySQL(app)

@app.route('/orders', methods=['GET', 'POST'])
def get_orders():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pemesanan")
    orders = cur.fetchall()
    cur.close()
    return render_template('getpemesanan.html', orders=orders)
    


@app.route('/armada', methods=['GET'])
def get_armada():
    resp = requests.get('http://localhost:3000/armada', verify=False)
    armada = resp.json()
    return render_template('getarmada.html', armada=armada)

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO pemesanan (nama_barang, pengirim, penerima, alamat_penerima, berat, jenis_kendaraan, tanggal_pemesanan) VALUES (%s, %s, %s, %s, %s, %s, %s)", (data['nama_barang'], data['pengirim'], data['penerima'], data['alamat_penerima'], data['berat'], data['jenis_kendaraan'], data['tanggal_pemesanan']))
    mysql.connection.commit()
    order_id = cur.lastrowid
    cur.close()
    return render_template('postpemesanan.html')


@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pemesanan WHERE id_pemesanan = %s", (order_id,))
    order = cur.fetchone()
    cur.close()
    if order:
        return jsonify(dict(zip(['id_pemesanan', 'nama_barang', 'pengirim', 'penerima', 'alamat_penerima', 'berat', 'jenis_kendaraan', 'tanggal_pemesanan'], order)))
    else:
        return jsonify({'message': 'Pemesanan tidak ditemukan'}), 404
    

@app.route('/orders/<int:order_id>', methods=['GET', 'PUT'])
def update_order(order_id):
    if request.method == 'PUT':
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE pemesanan SET nama_barang = %s, pengirim = %s, penerima = %s, alamat_penerima = %s, berat = %s, jenis_kendaraan = %s, tanggal_pemesanan = %s WHERE id_pemesanan = %s",
            (data['nama_barang'], data['pengirim'], data['penerima'], data['alamat_penerima'], data['berat'], data['jenis_kendaraan'], data['tanggal_pemesanan'], order_id)
        )
        mysql.connection.commit()
        cur.close()
        if cur.rowcount > 0:
            return jsonify({'message': 'Pemesanan berhasil diperbarui'})
        else:
            return jsonify({'message': 'Pemesanan tidak ditemukan'}), 404
    else:  # GET request
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM pemesanan WHERE id_pemesanan = %s", (order_id,))
        order_data = cur.fetchone()  # Ganti nama variabel menjadi order_data
        cur.close()

        if order_data:
            # Konversi order_data menjadi dictionary dengan nama kolom sebagai key
            order = dict(zip([column[0] for column in cur.description], order_data))
            return render_template('putpemesanan.html', order=order)  # Render template untuk edit
        else:
            return jsonify({'message': 'Pemesanan tidak ditemukan'}), 404




    


@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM pemesanan WHERE id_pemesanan = %s", (order_id,))
    mysql.connection.commit()
    cur.close()
    if cur.rowcount > 0:
        return jsonify({'message': 'Pemesanan berhasil dihapus'})
    else:
        return jsonify({'message': 'Pemesanan tidak ditemukan'}), 404
    

    
    



if __name__ == '__main__':
    app.run(debug=True, port=3000)
