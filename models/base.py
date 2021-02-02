import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

dir_path = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(dir_path, '../db.sqlite')
sqlitepath = f'sqlite:///{filepath}'
fresh_db = not os.path.exists(filepath)
engine = create_engine(sqlitepath, echo=False)
Base = declarative_base()
