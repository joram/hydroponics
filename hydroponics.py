import os

from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy

from models import fresh_db, Datapoint
from models.datapoint import start_polling
from flask_cors import CORS

app = Flask(__name__, static_folder="./hydroponics/build")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db.sqlite'
db = SQLAlchemy(app)
CORS(app)
if fresh_db:
    db.create_all()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def app_view(path):
    filepath = os.path.normpath(os.path.join(app.static_folder, path))
    print("serving %s" % filepath)
    if path != "" and os.path.exists(filepath):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/v0/data')
def data_view():
    data = []
    qs = db.session.query(Datapoint).order_by(Datapoint.created).all()
    for datapoint in qs:
        data.append({
            "name": f"{datapoint.created}",
            "PH": datapoint.ph,
            "Conductivity": datapoint.conductivity,
        })
    print(len(qs))
    return {"data": data}


start_polling()
app.run(host='0.0.0.0', port=8000)
