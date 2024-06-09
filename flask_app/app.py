# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from config import Config

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config.from_object(Config)

def get_db_connection():
    conn = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )
    return conn


@app.route('/')
def admin_landing():
    return render_template('admin_landing.html')

@app.route('/account')
def account():
    return render_template('account.html')


@app.route('/admin/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        required_fields = ['first_name', 'last_name', 'age', 'sex', 'identification_number', 'phone_number', 'address', 'next_of_kin_name', 'next_of_kin_phone', 'next_of_kin_address', 'next_of_kin_relation']
        for field in required_fields:
            if not request.form.get(field):
                flash(f"Field '{field}' is required.")
                return redirect(url_for('add_patient'))

        try:
            age = int(request.form['age'])
        except ValueError:
            flash("Age must be an integer.")
            return redirect(url_for('add_patient'))

        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'age': age,
            'sex': request.form['sex'],
            'identification_number': request.form['identification_number'],
            'phone_number': request.form['phone_number'],
            'address': request.form['address'],
            'insurance_number': request.form['insurance_number'],
            'insurance_company': request.form['insurance_company'],
            'insurance_type': request.form['insurance_type'],
            'next_of_kin_name': request.form['next_of_kin_name'],
            'next_of_kin_phone': request.form['next_of_kin_phone'],
            'next_of_kin_address': request.form['next_of_kin_address'],
            'next_of_kin_relation': request.form['next_of_kin_relation'],
            'icd10_code_main': request.form['icd10_code_main'],
            'icd10_main_symptoms': request.form['icd10_main_symptoms'],
            'icd10_code_secondary': request.form['icd10_code_secondary'],
            'icd10_secondary_symptoms': request.form['icd10_secondary_symptoms'],
            'primary_medication_name': request.form['primary_medication_name'],
            'primary_medication_purpose': request.form['primary_medication_purpose'],
            'primary_medication_dosage': request.form['primary_medication_dosage'],
            'primary_medication_side_effects': request.form['primary_medication_side_effects'],
            'primary_medication_drug_interactions': request.form['primary_medication_drug_interactions'],
            'primary_medication_food_interactions': request.form['primary_medication_food_interactions'],
            'secondary_medication_name': request.form['secondary_medication_name'],
            'secondary_medication_purpose': request.form['secondary_medication_purpose'],
            'secondary_medication_dosage': request.form['secondary_medication_dosage'],
            'secondary_medication_side_effects': request.form['secondary_medication_side_effects'],
            'secondary_medication_drug_interactions': request.form['secondary_medication_drug_interactions'],
            'secondary_medication_food_interactions': request.form['secondary_medication_food_interactions']
        }

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO patients (first_name, last_name, age, sex, identification_number, phone_number, address, 
                insurance_number, insurance_company, insurance_type, next_of_kin_name, next_of_kin_phone, 
                next_of_kin_address, next_of_kin_relation, icd10_code_main, icd10_main_symptoms, icd10_code_secondary, 
                icd10_secondary_symptoms, primary_medication_name, primary_medication_purpose, primary_medication_dosage, 
                primary_medication_side_effects, primary_medication_drug_interactions, primary_medication_food_interactions, 
                secondary_medication_name, secondary_medication_purpose, secondary_medication_dosage, 
                secondary_medication_side_effects, secondary_medication_drug_interactions, secondary_medication_food_interactions)
            VALUES (%(first_name)s, %(last_name)s, %(age)s, %(sex)s, %(identification_number)s, %(phone_number)s, %(address)s, 
                %(insurance_number)s, %(insurance_company)s, %(insurance_type)s, %(next_of_kin_name)s, %(next_of_kin_phone)s, 
                %(next_of_kin_address)s, %(next_of_kin_relation)s, %(icd10_code_main)s, %(icd10_main_symptoms)s, 
                %(icd10_code_secondary)s, %(icd10_secondary_symptoms)s, %(primary_medication_name)s, %(primary_medication_purpose)s, 
                %(primary_medication_dosage)s, %(primary_medication_side_effects)s, %(primary_medication_drug_interactions)s, 
                %(primary_medication_food_interactions)s, %(secondary_medication_name)s, %(secondary_medication_purpose)s, 
                %(secondary_medication_dosage)s, %(secondary_medication_side_effects)s, %(secondary_medication_drug_interactions)s, 
                %(secondary_medication_food_interactions)s)
        ''', data)
        conn.commit()
        cursor.close()
        conn.close()

        flash("Patient added successfully.")
        return redirect(url_for('add_patient'))
    return render_template('add_patient.html')

@app.route('/patient/<int:patient_id>')
def patient_view(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    print(f"Fetching data for patient_id: {patient_id}")  # Log patient ID
    cursor.execute('SELECT * FROM patients WHERE id = %s', (patient_id,))
    patient = cursor.fetchone()
    cursor.close()
    conn.close()

    if patient:
        print(f"Patient data: {patient}")  # Log fetched patient data
    else:
        print("No patient found with this ID.")

    return render_template('patient_view.html', patient=patient)

@app.route('/registered_patients')
def registered_patients():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Ensure the cursor returns dictionaries
    cursor.execute('SELECT * FROM patients')
    patients = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('registered_patients.html', patients=patients)

if __name__ == '__main__':
    app.run(debug=True)
