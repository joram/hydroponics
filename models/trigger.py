import datetime
import enum
import time

from sqlalchemy import Column, Integer, DateTime, String, Float, Enum, ForeignKey

from models import Datum, Session
from models.base import Base


class TriggerComparator(enum.Enum):
    GREATER_THAN = ">"
    LESS_THAN = "<"


class Trigger(Base):
    __tablename__ = 'triggers'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    name = Column(String)
    sensor = Column(ForeignKey("sensors.id"))
    threshold = Column(Float)
    comparator = Column(Enum(TriggerComparator))
    actuator = Column(ForeignKey("actuators.id"))
    on_duration_seconds = Column(Integer)
    period_seconds = Column(Integer)
    event_after = Column(DateTime, default=datetime.datetime.utcnow)

    def evaluate(self, datum: Datum):
        if datetime.datetime.now() < self.event_after:
            return

        if self.comparator == TriggerComparator.GREATER_THAN and datum.value > self.threshold:
            self.trigger_event()
            return

        if self.comparator == TriggerComparator.LESS_THAN and datum.value < self.threshold:
            self.trigger_event()

    def trigger_event(self):
        self.actuator.on()
        time.sleep(self.on_duration_seconds)
        self.event_after = datetime.datetime.now() + datetime.timedelta(seconds=self.period_seconds)
        self.actuator.off()

        session = Session()
        session.add(self)
        session.commit()

    def __repr__(self):
        return f"<Trigger name='{self.name}' />"
