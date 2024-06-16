
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app import db


db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
class VitalSigns(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    heart_rate = db.Column(db.Integer, nullable=False)
    blood_pressure = db.Column(db.String(20), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    patient = db.relationship('Patient', back_populates='vital_signs')

Patient.vital_signs = db.relationship('VitalSigns', order_by=VitalSigns.timestamp, back_populates='patient')


# Add the following line at the end of the file to import the existing models
from your_project.models import Patient  # replace your_project with your actual project name
