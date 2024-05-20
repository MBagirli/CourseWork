from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import hashlib
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    db = sqlite3.connect('/opt/render/project/src/Taxi_Service/Database/credentials.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    db.close()
    if user and hash_password(password) == user[2]:
        return True
    else:
        return False

def get_car_db_connection():
    conn = sqlite3.connect('/opt/render/project/src/Taxi_Service/Database/car_data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def initial():
    if session.get('user_id'):
        return redirect(url_for('home_page'))
    return render_template('index.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if session.get('user_id'):
        return redirect(url_for('home_page'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate_user(username, password):
            session['user_id'] = username
            session.permanent = True
            return redirect(url_for('home_page'))
    return render_template('signin.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if session.get('user_id'):
        return redirect(url_for('home_page'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = hash_password(password)
        if not authenticate_user(username, password):
            connection = sqlite3.connect('/opt/render/project/src/Taxi_Service/Database/credentials.db')
            cursor = connection.cursor()
            insert_user_query = '''
                INSERT INTO users (username, password_hash) VALUES (?, ?);
            '''
            cursor.execute(insert_user_query, (username, password_hash))
            connection.commit()
            connection.close()
            session['user_id'] = username
            session.permanent = True
            return redirect(url_for('home_page'))
    return render_template('signup.html')

@app.route('/home_page')
def home_page():
    return render_template('home_page.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signin'))

@app.route('/cars', methods=['GET'])
def get_cars():
    conn = get_car_db_connection()
    cursor = conn.cursor()
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=5, type=int)
    start = (page - 1) * per_page
    cursor.execute('SELECT * FROM car_info LIMIT ? OFFSET ?', (per_page, start))
    cars = cursor.fetchall()
    cursor.execute('SELECT COUNT(*) FROM car_info')
    total_records = cursor.fetchone()[0]
    has_next = (start + per_page) < total_records
    has_prev = start > 0
    conn.close()
    return jsonify({
        'cars': [dict(car) for car in cars],
        'has_next': bool(has_next),
        'has_prev': bool(has_prev)
    })

@app.route('/add_car_info', methods=['POST'])
def add_car_info():
    data = request.get_json()
    car_model = data.get('car_model')
    driver_name = data.get('driver_name')
    country_region = data.get('country_region')
    rating = data.get('rating')
    if not (car_model and driver_name and country_region and rating):
        return jsonify({'message': 'Missing Data!'})
    conn = sqlite3.connect('/opt/render/project/src/Taxi_Service/Database/car_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM car_info WHERE car_model=? AND driver_name=? AND country_region=?", (car_model, driver_name, country_region))
    existing_record = cursor.fetchone()
    if existing_record:
        conn.close()
        return jsonify({'message': 'Car information already exists in the database'}), 409
    cursor.execute("INSERT INTO car_info (car_model, driver_name, country_region, rating) VALUES (?, ?, ?, ?)", (car_model, driver_name, country_region, rating))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Car information added successfully! Please reload the page!'})

@app.route('/delete_element/<int:id>', methods=['DELETE'])
def delete_element(id):
    conn = sqlite3.connect('/opt/render/project/src/Taxi_Service/Database/car_data.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM car_info WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Element deleted successfully!'})

@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword', '')
    conn = sqlite3.connect('/opt/render/project/src/Taxi_Service/Database/car_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM car_info WHERE car_model LIKE ? OR driver_name LIKE ? OR country_region LIKE ? OR rating LIKE ?", 
               ("%" + keyword + "%", "%" + keyword + "%", "%" + keyword + "%", "%" + keyword + "%"))
    matched_records = cursor.fetchall()
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=5, type=int)
    start = (page - 1) * per_page
    end = start + per_page
    cars = matched_records[start:end]
    has_next = end < len(matched_records)
    has_prev = start > 0
    conn.close()
    return jsonify({
        'cars': [dict(zip([column[0] for column in cursor.description], car)) for car in cars],
        'has_next': has_next,
        'has_prev': has_prev
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
