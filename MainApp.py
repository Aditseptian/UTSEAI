from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/orders/<orders_id>)')
def get_orders(orders_id):
    orders_response = requests.get(f'')