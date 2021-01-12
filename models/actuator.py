import datetime

from sqlalchemy import Column, Integer, DateTime, String

from models.base import Base


class Actuator(Base):
    __tablename__ = 'actuators'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    name = Column(String)
    gpio_pin = Column(Integer)

    def __repr__(self):
        return f"<Actuator name='{self.name}' />"
