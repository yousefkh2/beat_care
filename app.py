from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from forms import LoginForm
from flask_migrate import Migrate
import pymysql
from datetime import datetime
from models import db, Patient, VitalSigns

# Initialize Flask application
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config.from_object(Config)

# Configure SQLAlchemy to use MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{user}:{password}@{host}/{db}'.format(
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    host=app.config['MYSQL_HOST'],
    db=app.config['MYSQL_DB']
)

db.init_app(app)

migrate = Migrate(app, db)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User model for authentication
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='scrypt')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


Patient.vital_signs = db.relationship('VitalSigns', order_by=VitalSigns.timestamp, back_populates='patient')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_landing'))
        elif current_user.role == 'patient':
            patient = Patient.query.filter_by(email=current_user.email).first()
            return redirect(url_for('patient_view', patient_id=patient.id))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('admin_landing'))
            elif user.role == 'patient':
                patient = Patient.query.filter_by(email=user.email).first()
                return redirect(url_for('patient_view', patient_id=patient.id))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/admin_landing')
@login_required
def admin_landing():
    if current_user.role != 'admin':
        return redirect(url_for('login'))
    return render_template('admin_landing.html')

@app.route('/admin/add_patient', methods=['GET', 'POST'])
@login_required
def add_patient():
    if current_user.role != 'admin':
        return redirect(url_for('login'))

    if request.method == 'POST':
        required_fields = [
            'first_name', 'last_name', 'age', 'sex', 'identification_number', 'phone_number', 'address',
            'next_of_kin_name', 'next_of_kin_phone', 'next_of_kin_address', 'next_of_kin_relation',
            'date_of_admission', 'email', 'password'
        ]
        for field in required_fields:
            if not request.form.get(field):
                flash(f"Field '{field}' is required.", 'danger')
                return redirect(url_for('add_patient'))

        try:
            age = int(request.form['age'])
        except ValueError:
            flash("Age must be an integer.", 'danger')
            return redirect(url_for('add_patient'))

        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'age': age,
            'sex': request.form['sex'],
            'identification_number': request.form['identification_number'],
            'phone_number': request.form['phone_number'],
            'address': request.form['address'],
            'date_of_admission': request.form['date_of_admission'],
            'insurance_number': request.form.get('insurance_number'),
            'insurance_company': request.form.get('insurance_company'),
            'insurance_type': request.form.get('insurance_type'),
            'next_of_kin_name': request.form['next_of_kin_name'],
            'next_of_kin_phone': request.form['next_of_kin_phone'],
            'next_of_kin_address': request.form['next_of_kin_address'],
            'next_of_kin_relation': request.form['next_of_kin_relation'],
            'icd10_code_main': request.form.get('icd10_code_main'),
            'icd10_main_symptoms': request.form.get('icd10_main_symptoms'),
            'icd10_code_secondary': request.form.get('icd10_code_secondary'),
            'icd10_secondary_symptoms': request.form.get('icd10_secondary_symptoms'),
            'primary_medication_name': request.form.get('primary_medication_name'),
            'primary_medication_purpose': request.form.get('primary_medication_purpose'),
            'primary_medication_dosage': request.form.get('primary_medication_dosage'),
            'primary_medication_side_effects': request.form.get('primary_medication_side_effects'),
            'primary_medication_drug_interactions': request.form.get('primary_medication_drug_interactions'),
            'primary_medication_food_interactions': request.form.get('primary_medication_food_interactions'),
            'secondary_medication_name': request.form.get('secondary_medication_name'),
            'secondary_medication_purpose': request.form.get('secondary_medication_purpose'),
            'secondary_medication_dosage': request.form.get('secondary_medication_dosage'),
            'secondary_medication_side_effects': request.form.get('secondary_medication_side_effects'),
            'secondary_medication_drug_interactions': request.form.get('secondary_medication_drug_interactions'),
            'secondary_medication_food_interactions': request.form.get('secondary_medication_food_interactions'),
            'email': request.form['email'],
            'password': request.form['password']
        }

        # Check if email already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            flash("Email address already in use.", 'danger')
            return redirect(url_for('add_patient'))

        # Add patient to database
        new_patient = Patient(
            first_name=data['first_name'],
            last_name=data['last_name'],
            age=data['age'],
            sex=data['sex'],
            identification_number=data['identification_number'],
            phone_number=data['phone_number'],
            address=data['address'],
            date_of_admission=data['date_of_admission'],
            insurance_number=data['insurance_number'],
            insurance_company=data['insurance_company'],
            insurance_type=data['insurance_type'],
            next_of_kin_name=data['next_of_kin_name'],
            next_of_kin_phone=data['next_of_kin_phone'],
            next_of_kin_address=data['next_of_kin_address'],
            next_of_kin_relation=data['next_of_kin_relation'],
            icd10_code_main=data['icd10_code_main'],
            icd10_main_symptoms=data['icd10_main_symptoms'],
            icd10_code_secondary=data['icd10_code_secondary'],
            icd10_secondary_symptoms=data['icd10_secondary_symptoms'],
            primary_medication_name=data['primary_medication_name'],
            primary_medication_purpose=data['primary_medication_purpose'],
            primary_medication_dosage=data['primary_medication_dosage'],
            primary_medication_side_effects=data['primary_medication_side_effects'],
            primary_medication_drug_interactions=data['primary_medication_drug_interactions'],
            primary_medication_food_interactions=data['primary_medication_food_interactions'],
            secondary_medication_name=data['secondary_medication_name'],
            secondary_medication_purpose=data['secondary_medication_purpose'],
            secondary_medication_dosage=data['secondary_medication_dosage'],
            secondary_medication_side_effects=data['secondary_medication_side_effects'],
            secondary_medication_drug_interactions=data['secondary_medication_drug_interactions'],
            secondary_medication_food_interactions=data['secondary_medication_food_interactions'],
            email=data['email'],
            password=data['password']
        )
        db.session.add(new_patient)

        # Add user account for patient
        new_user = User(email=data['email'], role='patient')
        new_user.set_password(data['password'])
        db.session.add(new_user)

        db.session.commit()

        flash("Patient added successfully.", 'success')
        return redirect(url_for('add_patient'))
    return render_template('add_patient.html')

@app.route('/patient/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def patient_view(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    if request.method == 'POST':
        heart_rate = request.form.get('heart_rate')
        blood_pressure = request.form.get('blood_pressure')
        temperature = request.form.get('temperature')
        
        if heart_rate and blood_pressure and temperature:
            new_vital_sign = VitalSigns(
                patient_id=patient_id,
                heart_rate=heart_rate,
                blood_pressure=blood_pressure,
                temperature=temperature
            )
            db.session.add(new_vital_sign)
            db.session.commit()
            flash('Vital signs submitted successfully.', 'success')
        else:
            flash('All fields are required.', 'danger')
        return redirect(url_for('patient_view', patient_id=patient_id))

    return render_template('patient_view.html', patient=patient)


@app.route('/admin/vital_signs')
@login_required
def admin_vital_signs():
    if current_user.role != 'admin':
        return redirect(url_for('login'))

    vital_signs = VitalSigns.query.all()
    return render_template('admin_vital_signs.html', vital_signs=vital_signs)

@app.route('/submit_vital_signs/<int:patient_id>', methods=['POST'])
@login_required
def submit_vital_signs(patient_id):
    if current_user.role != 'patient' or current_user.id != patient_id:
        return redirect(url_for('login'))

    heart_rate = request.form['heart_rate']
    blood_pressure = request.form['blood_pressure']
    temperature = request.form['temperature']

    new_vital_signs = VitalSigns(
        patient_id=patient_id,
        heart_rate=heart_rate,
        blood_pressure=blood_pressure,
        temperature=temperature
    )

    db.session.add(new_vital_signs)
    db.session.commit()

    flash("Vital signs submitted successfully.", 'success')
    return redirect(url_for('patient_view', patient_id=patient_id))

@app.route('/registered_patients')
@login_required
def registered_patients():
    if current_user.role != 'admin':
        flash('You do not have permission to view this page.', 'danger')
        return redirect(url_for('login'))
    
    patients = Patient.query.filter_by(is_active=True).all()
    return render_template('registered_patients.html', patients=patients)


@app.route('/delete_patient/<int:patient_id>', methods=['POST'])
@login_required
def delete_patient(patient_id):
    if current_user.role != 'admin':
        flash('You do not have permission to delete patients.', 'danger')
        return redirect(url_for('login'))

    patient = Patient.query.get_or_404(patient_id)
    try:
        patient.is_active = False
        db.session.commit()
        flash("Patient deleted successfully.", 'success')
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting patient: {str(e)}", 'danger')
    return redirect(url_for('registered_patients'))



@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
