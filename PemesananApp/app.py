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


@app.route('/orders', methods=['GET'])
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
    



@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute("UPDATE pemesanan SET nama_barang = %s, pengirim = %s, penerima = %s, alamat_penerima = %s, berat = %s, jenis_kendaraan = %s, tanggal_pemesanan = %s WHERE id_pemesanan = %s", (data['nama_barang'], data['pengirim'], data['penerima'], data['alamat_penerima'], data['berat'], data['jenis_kendaraan'], data['tanggal_pemesanan'], order_id))
    mysql.connection.commit()
    cur.close()
    if cur.rowcount > 0:
        return jsonify({'message': 'Pemesanan berhasil diperbarui'})
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
    
@app.route('/package', methods=['GET'])
def get_packages():
    cur = mysql.connection.cursor()
    
    # Mendapatkan parameter pencarian dari query string
    tracking_number = request.args.get('tracking_number')
    courier_name = request.args.get('courier_name')
    status = request.args.get('status')
    package_id = request.args.get('id')

    # Membuat query dasar
    query = 'SELECT id, tracking_number, courier_name, status, location FROM package WHERE 1'

    # Menambahkan filter ke query berdasarkan parameter pencarian yang diterima
    if package_id:
        query += f" AND id = {package_id}"
    if tracking_number:
        query += f" AND tracking_number = '{tracking_number}'"
    if courier_name:
        query += f" AND courier_name = '{courier_name}'"
    if status:
        query += f" AND status = '{status}'"

    cur.execute(query)
    packages = cur.fetchall()
    cur.close()

    package_list = []
    for package in packages:
        package_data = {
            'id': package[0],
            'tracking_number': package[1],
            'courier_name': package[2],
            'status': package[3],
            'location' : package[4]
        }
        package_list.append(package_data)

    response = {
        'status_code': 200,
        'message': 'Success',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'data': package_list
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)