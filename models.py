from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# class User(UserMixin, db.Model):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(150), unique=True, nullable=False)
#     password = db.Column(db.String(150), nullable=False)
#     role = db.Column(db.String(50), nullable=False)

#     def set_password(self, password):
#         self.password = generate_password_hash(password)

#     def check_password(self, password):
#         return check_password_hash(self.password, password)

class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    identification_number = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    date_of_admission = db.Column(db.Date, nullable=True)
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
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_active = db.Column(db.Boolean, default=True)  # New column to mark active/inactive status

    vital_signs = db.relationship('VitalSigns', back_populates='patient', cascade='all, delete-orphan')

class VitalSigns(db.Model):
    __tablename__ = 'vital_signs'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id', ondelete='CASCADE'), nullable=False)
    heart_rate = db.Column(db.Integer, nullable=False)
    blood_pressure = db.Column(db.String(20), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    patient = db.relationship('Patient', back_populates='vital_signs')
