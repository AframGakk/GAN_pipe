from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import environ

from Models.Entities.DataEntities import Base

class SqlEngine:
    def __init__(self):

        self.PGHOST = environ['PGHOST']
        self.PGDATABASE = environ['PGDATABASE']
        self.PGUSER = environ['PGUSER']
        self.PGPASSWORD = environ['PGPASSWORD']

        conn_string = "postgresql+psycopg2://{}:{}@{}/{}".format(self.PGUSER, self.PGPASSWORD, self.PGHOST, self.PGDATABASE)
        engine = create_engine(conn_string)

        # Bind the engine to the metadata of the Base class so that the
        # declaratives can be accessed through a DBSession instance
        Base.metadata.bind = engine

        self.DBSession = sessionmaker(bind=engine)

    def session(self):
        return self.DBSession()
