from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

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
    return jsonify([dict(zip(['id_pemesanan', 'nama_barang', 'pengirim', 'penerima', 'alamat_penerima', 'berat', 'jenis_kendaraan', 'tanggal_pemesanan'], order)) for order in orders])


@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO pemesanan (nama_barang, pengirim, penerima, alamat_penerima, berat, jenis_kendaraan, tanggal_pemesanan) VALUES (%s, %s, %s, %s, %s, %s, %s)", (data['nama_barang'], data['pengirim'], data['penerima'], data['alamat_penerima'], data['berat'], data['jenis_kendaraan'], data['tanggal_pemesanan']))
    mysql.connection.commit()
    order_id = cur.lastrowid
    cur.close()
    return jsonify({'message': 'Pemesanan berhasil dibuat', 'order_id': order_id})


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

if __name__ == '__main__':
    app.run(debug=True)