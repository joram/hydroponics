import datetime
import threading
import time

from sqlalchemy import Column, Integer, DateTime, Float, Boolean

from core import db
#from models import Session
#from models.base import Base
from utils.adc import read_analog_values


class Datapoint(db.Model):
    __tablename__ = 'datapoints'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    ph = Column(Float)
    conductivity = Column(Float)
    float = Column(Boolean)

    def __repr__(self):
        return f"<Datapoint created='{self.created}' ph='{self.ph}' conductivity='{self.conductivity}' />"

    def evaluate_triggers(self):
        if self.ph > 1:
            print("raise PH")
        if self.ph < 1:
            print("lower PH")
        if self.conductivity > 1:
            print("raise nutrients")
        raise NotImplementedError()

    @classmethod
    def create(cls):
        [ph, conductivity] = read_analog_values([7, 6])
        return Datapoint(
            created=datetime.datetime.now(),
            ph=ph,
            conductivity=conductivity,
            float=True,
        )

db.create_all()
thread = None
kill_thread = False


def start_polling(wait=5):
    global thread
    global kill_thread
    if thread is not None:
        return

    def _polling():
        while not kill_thread:
            datapoint = Datapoint.create()
            print(datapoint)
            db.session.add(datapoint)
            db.session.commit()
            time.sleep(wait)

    kill_thread = False
    thread = threading.Thread(target=_polling)
    thread.start()


def stop_polling():
    global thread
    global kill_thread

    if thread is None:
        return

    kill_thread = True
    thread.join()
    thread = None
