
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
import jwt
from functools import wraps

app = Flask(__name__)

# Konfigurasi MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'logistik'

mysql = MySQL(app)

# Konfigurasi JWT
SECRET_KEY = "your_super_secret_key"  
ALGORITHM = "HS256"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            print("Header Auth:", request.headers['Authorization'])  # Tambahkan ini
            token = request.headers['Authorization'].split()[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token is expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(*args, **kwargs)
    return decorated

@app.route('/api/orders', methods=['GET'])
@token_required
def get_orders():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pemesanan")
    orders = cur.fetchall()
    cur.close()
    orders_list = [
        dict(zip(['id_pemesanan', 'nama_barang', 'pengirim', 'penerima', 'alamat_penerima', 'berat', 'jenis_kendaraan', 'tanggal_pemesanan'], order))
        for order in orders
    ]
    return jsonify(orders_list)

@app.route('/api/orders', methods=['POST'])
@token_required
def create_order():
    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO pemesanan (nama_barang, pengirim, penerima, alamat_penerima, berat, jenis_kendaraan, tanggal_pemesanan) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (data['nama_barang'], data['pengirim'], data['penerima'], data['alamat_penerima'], data['berat'], data['jenis_kendaraan'], data['tanggal_pemesanan'])
    )
    mysql.connection.commit()
    order_id = cur.lastrowid
    cur.close()
    return jsonify({'id_pemesanan': order_id, 'message': 'Order created successfully'})

@app.route('/api/orders/<int:order_id>', methods=['GET'])
@token_required
def get_order(order_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pemesanan WHERE id_pemesanan = %s", (order_id,))
    order = cur.fetchone()
    cur.close()
    if order:
        return jsonify(dict(zip(['id_pemesanan', 'nama_barang', 'pengirim', 'penerima', 'alamat_penerima', 'berat', 'jenis_kendaraan', 'tanggal_pemesanan'], order)))
    else:
        return jsonify({'message': 'Pemesanan tidak ditemukan'}), 404

@app.route('/api/orders/<int:order_id>', methods=['PUT'])
@token_required
def edit_order(order_id):
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

@app.route('/api/orders/<int:order_id>', methods=['DELETE'])
@token_required
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
    app.run(debug=True, port=5001)