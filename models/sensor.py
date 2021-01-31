import datetime
import enum
import threading
import time

import board
import busio
from adafruit_bus_device.i2c_device import I2CDevice
from sqlalchemy import Column, Integer, DateTime, String, Enum

from models import Session, Datum, engine
from models.base import Base
from models.trigger import Trigger


class SensorType(enum.Enum):
    SWITCH = "switch"
    I2C = "i2c"


class Sensor(Base):
    __tablename__ = 'sensors'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    name = Column(String)
    gpio_pin = Column(Integer)
    i2c_address = Column(Integer)
    wait = Column(Integer)
    last_reading_at = Column(DateTime, default=datetime.datetime.utcnow)
    sensor_type = Column(Enum(SensorType))
    polling_period_seconds = Column(Integer)

    thread = None
    kill_thread = False

    def __repr__(self):
        return f"<Sensor name='{self.name}' />"

    def bytes_to_float(self, data):
        value = data[0] << 8 | data[1]
        temp = (value & 0xFFF) / 16.0
        if value & 0x1000:
            temp -= 256.0
        return temp

    def read_value(self):
        bytes_read = bytearray(4)
        with busio.I2C(busio.SCL, board.SDA) as i2c:
            device = I2CDevice(i2c, self.i2c_address)
            with device:
                device.readinto(bytes_read)
        return self.bytes_to_float(bytes_read)

    def start_polling(self):
        if self.thread is not None:
            return

        def _polling():
            while not self.kill_thread:
                datum = Datum(value=self.read_value())
                session = Session()
                session.add(datum)
                session.commit()

                triggers = session.query(Trigger).filter(Trigger.sensor == self.id)
                for trigger in triggers:
                    trigger.evaluate(datum)

                time.sleep(self.wait)

        self.kill_thread = False
        self.thread = threading.Thread(target=_polling)
        self.thread.start()

    def stop_polling(self):
        if self.thread is None:
            return

        self.kill_thread = True
        self.thread.join()
        self.thread = None


def start_polling_all_sensors():
    Base.metadata.create_all(engine)
    session = Session()
    sensors = session.query(Sensor)
    for sensor in sensors:
        sensor.start_polling()
