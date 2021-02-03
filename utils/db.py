from models import Base, engine


def setup_new_db():
    Base.metadata.create_all(engine)

