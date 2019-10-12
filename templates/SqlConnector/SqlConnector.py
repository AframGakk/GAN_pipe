import psycopg2
import pandas as pd
import configparser
import traceback

config = configparser.ConfigParser()

class SqlConnector:
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


    def getEngine(self):
        conn_string = "host=" + self.PGHOST + " port=" + "5432" + " dbname=" + self.PGDATABASE + " user=" + self.PGUSER \
                      + " password=" + self.PGPASSWORD

        conn = psycopg2.connect(conn_string)

        return conn


    def load_query(self, query):
        try:
            conn = self.getEngine()
        except Exception:
            print('Cannot fetch connection')
            return None

        data = pd.read_sql(query, conn)


        return data

    def insert_query(self, query, values):
        try:
            conn = self.getEngine()
            cur = conn.cursor()
            cur.execute(query, values)
            id = cur.fetchone()[0]
            conn.commit()
            cur.close()
        except Exception:
            print('Cannot fetch connection')
            return None
        finally:
            if conn is not None:
                conn.close()

        return id

    def delete_query(self, table, id):
        query = "DELETE FROM {} WHERE id = %s".format(table)
        try:
            conn = self.getEngine()
            cur = conn.cursor()
            cur.execute(query, (id,))
            rows_deleted = cur.rowcount
            conn.commit()
            cur.close()
        except Exception:
            print('Cannot fetch connection')
            return None
        finally:
            if conn is not None:
                conn.close()

        return id

    def update_table(self, table, id, values):
        set_string = ''
        for i, item in enumerate(values):
            set_string = set_string + '{} = \'{}\''.format(item[0], item[1])
            if i != len(values) - 1:
                set_string = set_string + ', '
            else:
                set_string = set_string + ' '

        query = """ UPDATE {} SET {} WHERE id = %s""".format(table, set_string)

        try:
            conn = self.getEngine()
            cur = conn.cursor()
            # execute the UPDATE  statement
            cur.execute(query, (id,))
            # get the number of updated rows
            updated_rows = cur.rowcount
            conn.commit()
            # Close communication with the PostgreSQL database
            cur.close()
        except Exception:
            print('Update connection not completed')
            return False
        finally:
            if conn is not None:
                conn.close()

        return True

