from flask import Flask, request, jsonify, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import pickle
import joblib
import numpy as np
import os
import MySQLdb.cursors
import re

from sklearn.metrics import accuracy_score

model = pickle.load(open('D:/Fay/1,2,2.3/4.1/SP/models/model.pkl', 'rb'))

app = Flask(__name__)

app.secret_key = 'xyz'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'user-system'

mysql = MySQL(app)

"""@app.route('/')
def index():
    return render_template("homepage.html")"""

@app.route('/')
def index():
    return render_template("homepage.html")

@app.route('/fast')
def fast():
    return render_template("fast.html")

@app.route('/manage')
def manage():
    return render_template("manage.html")

@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        userName = request.form['name']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s , % s, % s)', (userName, email, password, confirm_password, ))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register.html', mesage = mesage)


@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            mesage = 'Logged in successfully !'
            return render_template('home.html', mesage = mesage)
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('index'))


class Y_pred:
    pass

class Y_test:
    pass


@app.route("/result", methods=['POST', 'GET'])
def result():
    gender = request.form.get('gender')
    age = request.form.get('age')
    hypertension = request.form.get('hypertension')
    heart_disease = request.form.get('heart_disease')
    ever_married = request.form.get('ever_married')
    work_type = request.form.get('work_type')
    Residence_type = request.form.get('Residence_type')
    avg_glucose_level = request.form.get('avg_glucose_level')
    bmi = request.form.get('bmi')
    smoking_status = request.form.get('smoking_status')

    x = np.array([gender, age, hypertension, heart_disease, ever_married, work_type, Residence_type,
                  avg_glucose_level, bmi, smoking_status]).reshape(1, -1)


    model_path = os.path.join('D:/Fay/1,2,2.3/4.1/SP/', 'models/model.pkl')
    # dt = joblib.load(model_path)

    #dt = joblib.load(model_path)

    #Y_pred = dt.predict(x)
    model = joblib.load("models/model.pkl")

    Y_pred = model.predict(x)


    print('PREDICTION IN PERCENTAGE', Y_pred)

    # for No Stroke Risk
    if Y_pred == 0:
        return render_template('nostroke.html')
    else:
        return render_template('stroke.html')



if __name__ == "__main__":
    app.run(debug=True, port=7384)

