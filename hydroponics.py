import os

from flask import Flask, send_from_directory

from models import fresh_db, Session, Base, engine, Datum
from models.sensor import start_polling_all_sensors
from utils import setup_new_db
from flask_cors import CORS

app = Flask(__name__, static_folder="./hydroponics/build")
CORS(app)
if fresh_db:
    setup_new_db()


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
    Base.metadata.create_all(engine)
    session = Session()
    data = session.query(Datum).order_by(Datum.created)
    return {"data": [{"name": 'datum', "value": datum.value} for datum in data]}


start_polling_all_sensors()
app.run(host='0.0.0.0', port=8000)