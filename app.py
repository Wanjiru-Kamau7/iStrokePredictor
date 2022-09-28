from flask import Flask, request, jsonify
import pickle
import numpy as np
import os

model = pickle.load(open('D:/Fay/1,2,2.3/4.1/SP/models/model.pkl', 'rb'))

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello World"


@app.route('/predict', methods=['POST'])
def predict():
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

    input_query = np.array([[gender, age, hypertension, heart_disease, ever_married, work_type, Residence_type,
                             avg_glucose_level, bmi, smoking_status]])

    result = model.predict(input_query)[0]
    return jsonify({'result': str(result)})


if __name__ == '__main__':
    app.run(debug=True, port=8080, use_reloader=False)


