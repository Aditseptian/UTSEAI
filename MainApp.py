# MainApp.py
from flask import Flask, redirect, render_template, jsonify, request, url_for
import requests
from auth import generate_token

app = Flask(__name__)

PEMESANAN_APP_URL = 'http://127.0.0.1:5001/api/orders'

def get_headers():
    token = generate_token()
    print("Generated Token:", token)  # Tambahkan ini
    return {"Authorization": f"Bearer {token}"}



@app.route('/')
def index():
    response = requests.get(PEMESANAN_APP_URL, headers=get_headers())
    if response.status_code == 200:
        orders = response.json()
    else:
        orders = []
    return render_template('index.html', orders=orders)

@app.route('/orders')
def view_orders():
    response = requests.get(PEMESANAN_APP_URL, headers=get_headers())
    if response.status_code == 200:
        orders = response.json()
    else:
        orders = []
    return render_template('getpemesanan.html', orders=orders)

@app.route('/create_order', methods=['GET', 'POST'])
def create_order():
    if request.method == 'POST':
        data = request.form.to_dict()
        response = requests.post(PEMESANAN_APP_URL, json=data, headers=get_headers())
        if response.status_code == 200:
            return redirect(url_for('index'))
        else:
            return jsonify({'message': 'Failed to create order'}), 500
    return render_template('postpemesanan.html')

@app.route('/edit_order/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):
    if request.method == 'POST':
        data = request.form.to_dict()
        response = requests.put(f'{PEMESANAN_APP_URL}/{order_id}', json=data, headers=get_headers())
        if response.status_code == 200:
            return redirect('/')
        else:
            return jsonify({'message': 'Failed to update order'}), 500
    else:
        response = requests.get(f'{PEMESANAN_APP_URL}/{order_id}', headers=get_headers())
        if response.status_code == 200:
            order = response.json()
            return render_template('putpemesanan.html', order=order)
        else:
            return jsonify({'message': 'Pemesanan tidak ditemukan'}), 404

@app.route('/delete_order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    response = requests.delete(f'{PEMESANAN_APP_URL}/{order_id}', headers=get_headers())
    if response.status_code == 200:
        return redirect('/')
    else:
        return jsonify({'message': 'Failed to delete order'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)