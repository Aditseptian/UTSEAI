from flask import Flask, redirect, render_template, jsonify, request, url_for
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
    response = requests.get('http://127.0.0.1:3000/orders')
    return response.json(), response.status_code

# Rute untuk membuat pesanan baru
@app.route('/create_order', methods=['GET', 'POST'])
def create_order():
    if request.method == 'POST':
        data = request.form
        response = requests.post('http://127.0.0.1:3000/orders', json=data)
        return redirect(f'http://127.0.0.1:3000/orders/{response.json()["id_pemesanan"]}')  # Redirect ke halaman detail pesanan di port 3000
    return render_template('postpemesanan.html')

# Rute untuk mendapatkan detail pesanan
@app.route('/orders/<int:order_id>')
def get_order(order_id):
    orders_response = requests.get(f'http://127.0.0.1:3000/orders/{order_id}')
    return orders_response.json(), orders_response.status_code

# Rute untuk mengupdate pesanan
@app.route('/update_order/<int:order_id>', methods=['GET', 'POST'])
def update_order(order_id):
    if request.method == 'POST':
        data = request.form
        response = requests.put(f'http://127.0.0.1:3000/orders/{order_id}', json=data)
        return redirect(f'http://127.0.0.1:3000/orders/{order_id}')  # Redirect ke halaman detail pesanan di port 3000
    response = requests.get(f'http://127.0.0.1:3000/orders/{order_id}')
    order = response.json()
    return render_template('putpemesanan.html', order=order)

@app.route('/delete_order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    orders_response = requests.delete(f'http://127.0.0.1:3000/orders/{order_id}')
    return redirect(url_for('index'))

# Rute untuk mendapatkan paket
@app.route('/package')
def get_packages():
    try:
        packages_response = requests.get('http://127.0.0.1:3001/package')
        packages_response.raise_for_status()  # Raise error jika status code bukan 200
        return render_template('getpelacakan.html')
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch package data"}), 500


if __name__ == '__main__':
    app.run(debug=True)
