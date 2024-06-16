# config.py

import os

class Config:
    MYSQL_HOST = os.getenv('MYSQLHOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQLUSER', 'admin')
    MYSQL_PASSWORD = os.getenv('MYSQLPASSWORD', 'password123')
    MYSQL_DB = os.getenv('MYSQLDATABASE', 'your_database')
    MYSQL_CURSORCLASS = 'DictCursor'

