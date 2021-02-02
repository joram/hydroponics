import os

from flask import Flask, send_from_directory

from models import fresh_db, Session, Base, engine, Datum, DatumGroup, Sensor
from models.sensor import start_polling
from utils.db import setup_new_db
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
    datum_groups = session.query(DatumGroup).order_by(DatumGroup.created).all()
    data = []
    for dg in datum_groups:
        datapoint = {"name":f"{dg.created}"}
        qs = session.query(Datum).filter_by(datum_group_id=dg.id).all()
        for datum in qs:
            sensor = session.query(Sensor).filter_by(id=datum.sensor_id).all()[0]
            datapoint[sensor.name] = datum.value
        data.append(datapoint)
    return {"data": data}


start_polling()
app.run(host='0.0.0.0', port=8000)
