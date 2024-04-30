from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # Di sini Anda harus mengganti metode ini dengan metode yang sesuai untuk mendapatkan data pesanan dari database atau sumber data lainnya.
    # Misalnya, Anda dapat mengambil data pesanan dari database menggunakan SQLAlchemy atau menggunakan sumber data lainnya.
    # Kemudian, Anda dapat mengirimkan data tersebut ke template menggunakan argumen `orders`.
    orders = [
        {'id_pemesanan': 1, 'nama_barang': 'Barang 1', 'pengirim': 'Pengirim 1', 'penerima': 'Penerima 1', 'alamat_penerima': 'Alamat Penerima 1', 'berat': 1.5, 'jenis_kendaraan': 'Truk', 'tanggal_pemesanan': '2024-04-30'},
        {'id_pemesanan': 2, 'nama_barang': 'Barang 2', 'pengirim': 'Pengirim 2', 'penerima': 'Penerima 2', 'alamat_penerima': 'Alamat Penerima 2', 'berat': 2.0, 'jenis_kendaraan': 'Mobil', 'tanggal_pemesanan': '2024-04-29'}
    ]
    return render_template('index.html', orders=orders)
# Rute untuk mendapatkan semua pesanan
@app.route('/orders', methods=['GET'])
def get_orders():
    orders_response = requests.get(f'http://127.0.0.1:5000/orders')
    return orders_response.json()

# Rute untuk membuat pesanan baru
@app.route('/orders', methods=['POST'])
def create_order():
    data = requests.get_json()
    orders_response = requests.post('http://127.0.0.1:5000/orders', json=data)
    return orders_response.json(), orders_response.status_code

# Rute untuk mendapatkan detail pesanan
@app.route('/orders/<int:order_id>')
def get_order(order_id):
    orders_response = requests.get(f'http://127.0.0.1:5000/orders/{order_id}')
    return orders_response.json(), orders_response.status_code

# Rute untuk mengupdate pesanan
@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = requests.get_json()
    orders_response = requests.put(f'http://127.0.0.1:5000/orders/{order_id}', json=data)
    return orders_response.json(), orders_response.status_code

# Rute untuk menghapus pesanan
@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    orders_response = requests.delete(f'http://127.0.0.1:5000/orders/{order_id}')
    return orders_response.json(), orders_response.status_code

# Rute untuk mendapatkan paket
@app.route('/package')
def get_packages():
    packages_response = requests.get('http://127.0.0.1:5000/package')
    return packages_response.json(), packages_response.status_code

if __name__ == '__main__':
    app.run(debug=True)
