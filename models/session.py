from sqlalchemy.orm import sessionmaker
from .base import engine

Session = sessionmaker(bind=engine)

