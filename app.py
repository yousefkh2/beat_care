from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from forms import LoginForm
from flask_migrate import Migrate
import pymysql

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
db = SQLAlchemy(app)
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
        self.password = generate_password_hash(password)

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

# Patient model
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    identification_number = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    insurance_number = db.Column(db.String(50), nullable=True)
    insurance_company = db.Column(db.String(255), nullable=True)
    insurance_type = db.Column(db.String(50), nullable=True)
    next_of_kin_name = db.Column(db.String(255), nullable=True)
    next_of_kin_phone = db.Column(db.String(50), nullable=True)
    next_of_kin_address = db.Column(db.String(255), nullable=True)
    next_of_kin_relation = db.Column(db.String(50), nullable=True)
    icd10_code_main = db.Column(db.String(50), nullable=True)
    icd10_main_symptoms = db.Column(db.Text, nullable=True)
    icd10_code_secondary = db.Column(db.String(50), nullable=True)
    icd10_secondary_symptoms = db.Column(db.Text, nullable=True)
    primary_medication_name = db.Column(db.String(255), nullable=True)
    primary_medication_purpose = db.Column(db.Text, nullable=True)
    primary_medication_dosage = db.Column(db.Text, nullable=True)
    primary_medication_side_effects = db.Column(db.Text, nullable=True)
    primary_medication_drug_interactions = db.Column(db.Text, nullable=True)
    primary_medication_food_interactions = db.Column(db.Text, nullable=True)
    secondary_medication_name = db.Column(db.String(255), nullable=True)
    secondary_medication_purpose = db.Column(db.Text, nullable=True)
    secondary_medication_dosage = db.Column(db.Text, nullable=True)
    secondary_medication_side_effects = db.Column(db.Text, nullable=True)
    secondary_medication_drug_interactions = db.Column(db.Text, nullable=True)
    secondary_medication_food_interactions = db.Column(db.Text, nullable=True)
    date_of_admission = db.Column(db.Date, nullable=True)
    email = db.Column(db.String(150), unique=True, nullable=False)  # Add this line


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Login route
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
                return redirect(url_for('patient_view', patient_id=user.id))
            else:
                flash('Invalid role.', 'danger')
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/')
@login_required
def admin_landing():
    if current_user.role != 'admin':
        return redirect(url_for('login'))
    return render_template('admin_landing.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin/add_patient', methods=['GET', 'POST'])
@login_required
def add_patient():
    if current_user.role != 'admin':
        return redirect(url_for('login'))
    if request.method == 'POST':
        required_fields = ['first_name', 'last_name', 'age', 'sex', 'identification_number', 'phone_number', 'address', 'next_of_kin_name', 'next_of_kin_phone', 'next_of_kin_address', 'next_of_kin_relation', 'date_of_admission', 'email', 'password']
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
            'date_of_admission': request.form['date_of_admission'],
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
            'secondary_medication_food_interactions': request.form['secondary_medication_food_interactions'],
            'email': request.form['email']
        }

        new_patient = Patient(**data)
        db.session.add(new_patient)
        db.session.commit()

        # Create user account for patient
        patient_email = request.form['email']
        patient_password = request.form['password']  # Use the password provided by the admin
        new_user = User(email=patient_email, role='patient')
        new_user.set_password(patient_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Patient added and user account created successfully.")
        return redirect(url_for('add_patient'))
    return render_template('add_patient.html')



@app.route('/patient/<int:patient_id>')
@login_required
def patient_view(patient_id):
    if current_user.role != 'patient' or current_user.id != patient_id:
        return redirect(url_for('login'))
    patient = Patient.query.get_or_404(patient_id)
    if patient:
        print(f"Patient data: {patient}")  # Log fetched patient data
    else:
        print("No patient found with this ID.")
    return render_template('patient_view.html', patient=patient)


@app.route('/registered_patients')
@login_required
def registered_patients():
    if current_user.role != 'admin':
        return redirect(url_for('login'))
    patients = Patient.query.all()
    return render_template('registered_patients.html', patients=patients)

if __name__ == '__main__':
    app.run(debug=True)
