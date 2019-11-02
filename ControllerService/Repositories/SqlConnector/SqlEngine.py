from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import configparser
import traceback

config = configparser.ConfigParser()

from Models.Entities.DataEntities import Base

class SqlEngine:
    def __init__(self):

        try:
            config.read('./config/config.ini')
            self.PGHOST = config['SQL_CONNECTOR']['PGHOST']
            self.PGDATABASE = config['SQL_CONNECTOR']['PGDATABASE']
            self.PGUSER = config['SQL_CONNECTOR']['PGUSER']
            self.PGPASSWORD = config['SQL_CONNECTOR']['PGPASSWORD']
        except:
            print('could not load config file!')
            print(traceback.print_exc())

        conn_string = "postgresql+psycopg2://{}:{}@{}/{}".format(self.PGUSER, self.PGPASSWORD, self.PGHOST, self.PGDATABASE)
        engine = create_engine(conn_string)

        # Bind the engine to the metadata of the Base class so that the
        # declaratives can be accessed through a DBSession instance
        Base.metadata.bind = engine

        self.DBSession = sessionmaker(bind=engine)

    def session(self):
        return self.DBSession()
