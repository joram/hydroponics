import os

from core import app, db
from models import Datapoint
from models.datapoint import start_polling

from flask import send_from_directory

dir_path = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(dir_path, './db.sqlite')
if not os.path.exists(filepath):
    print("creating db")
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
            "name": datapoint.created.strftime('%H:%M:%S%p'),
            "PH": datapoint.ph,
            "Conductivity": datapoint.conductivity,
        })
    print(len(qs))
    return {"data": data}


if __name__ == "__main__":
    start_polling()
    app.run(host='0.0.0.0', port=8000)
