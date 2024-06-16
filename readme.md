# Beat Care

Beat Care is a web application designed to manage patient information, specifically focused on cardiac care. The application provides features for patient registration, viewing registered patients, and managing user roles (admin and patient).

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Routes](#routes)
- [License](#license)

## Features

- User authentication and authorization
- Admin and patient roles
- Patient registration with detailed medical information
- Viewing registered patients
- Deleting patients
- Flash messages for feedback
- Responsive design with Tailwind CSS

## Technologies Used

- Flask
- Flask-SQLAlchemy
- Flask-WTF
- Flask-Login
- MySQL
- Tailwind CSS

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/yousefkh2/beat_care.git
   cd beat_care
2. **Create a virtual environment**:
```sh
python3 -m venv venv
source venv/bin/activate
```
3. **Install the dependencies**
```sh
pip install -r requirements.txt
```
4. **Set up the database:**
- Make sure you have MySQL installed and running.
- Create a new database named your_database (or use another name, but update your config accordingly).
5. **Configure the application:**
- Update the config.py file with your MySQL database credentials.
- Example config.py:
```python
import os

class Config:
    MYSQL_HOST = os.getenv('MYSQLHOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQLUSER', 'admin')
    MYSQL_PASSWORD = os.getenv('MYSQLPASSWORD', 'password123')
    MYSQL_DB = os.getenv('MYSQLDATABASE', 'your_database')
    MYSQL_CURSORCLASS = 'DictCursor'
    SECRET_KEY = 'your_secret_key'
```
6. **Create the database tables:**
```sh
flask db upgrade
```
7. **Run the application:**
```sh
flask run
```

## Usage
### Admin Login:
- Email: admin@example.com
- Password: 123456
### Adding Patients:
- Navigate to the "Patient Registration" page to add new patients.
### Viewing Registered Patients:
- Navigate to the "Registered Patients" page to view and delete patients.

## Routes
- / - Admin landing page
- /login - Login page
- /logout - Logout route
- /admin/add_patient - Add patient page (admin only)
- /patient/<int:patient_id> - View patient details (patient only)
- /registered_patients - View all registered patients (admin only)
- /about - About page
## License
This project is licensed under the MIT License. See the LICENSE file for details.