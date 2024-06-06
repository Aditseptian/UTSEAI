from flask import Flask, jsonify, request
from flask import render_template
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)
#database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'package'


mysql = MySQL(app)


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
    return render_template('getpelacakan.html', packages =package_list)


if __name__ == '__main__':
    app.run(debug=True, port=3001)