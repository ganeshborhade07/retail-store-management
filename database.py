from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

DATABASE_URL = "sqlite:///retail_db.db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

write_engine = None
read_engine = None

def initialize_engine(connection_string):
    global write_engine
    if not write_engine:
        write_engine = create_engine(connection_string)
    return write_engine

def initialize_read_engine(connection_string):
    global read_engine
    if not read_engine:
        read_engine = create_engine(connection_string)
    return read_engine

class RoutingSession(Session):

    def get_bind(self, mapper=None, clause=None):
        if self._flushing:
            return initialize_engine(DATABASE_URL)
        else:
            return initialize_read_engine(DATABASE_URL)

class Backend(object):
    def __init__(self):
        self._engine = initialize_engine(DATABASE_URL)

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def get_engine(self):
        return self._engine
    
    def get_session_factory(self):
        self._session_factory = scoped_session(sessionmaker(bind=self._engine))
        return self._session_factory

    def get_session(self):
        self.get_session_factory()
        self._session = self._session_factory()
        return self._session

    def get_new_session_factory(self):
        self._session_factory = scoped_session(sessionmaker(class_=RoutingSession))
        return self._session_factory

    def get_new_session(self):
        self.get_new_session_factory()
        self._session = self._session_factory()
        return self._session
