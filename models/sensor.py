import datetime
import enum
import threading
import time

import board
import busio
from adafruit_bus_device.i2c_device import I2CDevice
from sqlalchemy import Column, Integer, DateTime, String, Enum

from models import Session, DatumGroup, Datum, engine
from models.base import Base
from models.trigger import Trigger
from utils.adc import read_analog_value


class SensorType(enum.Enum):
    SWITCH = "switch"
    I2C = "i2c"
    ANALOG = "analog"


class Sensor(Base):
    __tablename__ = 'sensors'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    name = Column(String)
    gpio_pin = Column(Integer)
    i2c_address = Column(Integer)
    last_reading_at = Column(DateTime, default=datetime.datetime.utcnow)
    sensor_type = Column(Enum(SensorType))
    polling_period_seconds = Column(Integer)


    def __repr__(self):
        return f"<Sensor name='{self.name}' />"

    def bytes_to_float(self, data):
        value = data[0] << 8 | data[1]
        temp = (value & 0xFFF) / 16.0
        if value & 0x1000:
            temp -= 256.0
        return temp

    def _read_analog_value(self) -> float:
        return read_analog_value(self.gpio_pin)

    def _read_i2c_value(self) -> float:
        bytes_read = bytearray(4)
        with busio.I2C(busio.SCL, board.SDA) as i2c:
            device = I2CDevice(i2c, self.i2c_address)
            with device:
                device.readinto(bytes_read)
        return self.bytes_to_float(bytes_read)

    def read_value(self) -> float:
        if self.sensor_type == SensorType.I2C:
            return self._read_i2c_value()

        if self.sensor_type == SensorType.ANALOG:
            return self._read_analog_value()

wait = 5
thread = None
kill_thread = False


def start_polling():
    global thread
    global kill_thread
    global wait

    if thread is not None:
        return

    def _polling():
        while not kill_thread:
            session = Session()
            sensors = session.query(Sensor).all()
            datum_group = DatumGroup()
            session.add(datum_group)
            for sensor in sensors:
                datum = Datum(value=sensor.read_value(), sensor_id=sensor.id, datum_group_id=datum_group.id)
                print(f"sensor:{sensor}, value:{datum.value}")
                session.add(datum)
            
                triggers = session.query(Trigger).filter(Trigger.sensor == sensor.id)
                for trigger in triggers:
                    trigger.evaluate(datum)

            session.commit()
            time.sleep(wait)

    kill_thread = False
    thread = threading.Thread(target=_polling)
    thread.start()

def stop_polling():
    if thread is None:
        return

    kill_thread = True
    thread.join()
    thread = None

