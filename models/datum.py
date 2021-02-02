import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float

from models.base import Base


class DatumGroup(Base):
    __tablename__ = 'data_group'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f"<DataGroup create='{self.created}' />"

class Datum(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    sensor_id = Column(ForeignKey("sensors.id"))
    data_group_id = Column(ForeignKey("data_group.id"))
    value = Column(Float)

    def __repr__(self):
        return f"<Datum name='{self.value}' />"
