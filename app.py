from flask import Flask, render_template, session, url_for, redirect, request, jsonify
from pages import page
from db import init_db
import uuid
from datetime import datetime, timedelta
import base64
from openpyxl import load_workbook
import os
from helpers import *




app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')


app.config['MYSQL_HOST'] = os.environ.get('DBHOST')
app.config["MYSQL_USER"] = "root"       
app.config["MYSQL_PASSWORD"] = os.environ.get('DBPASSWORD')
app.config["MYSQL_DB"] = "tulsiyandb"

#initializing database
init_db(app)

app.register_blueprint(page)



if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
