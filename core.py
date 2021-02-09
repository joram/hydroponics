import os

from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

dir_path = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__, static_folder="./hydroponics/build")
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(dir_path, "db.sqlite")}'
CORS(app)

db = SQLAlchemy(app)


