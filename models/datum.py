import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float

from models.base import Base
import sys
#import fake_rpi

#sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi
#sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO # Fake GPIO


class Datum(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    sensor_id = Column(ForeignKey("sensors.id"))
    value = Column(Float)

    def __repr__(self):
        return f"<Sensor name='{self.name}' />"

    def poll(self):
        GPIO.setup(0, GPIO.IN)
        input = GPIO.input(0)
