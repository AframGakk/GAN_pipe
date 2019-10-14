from unittest import TestCase
import os

from SqlConnector.SqlConnector import SqlConnector

os.chdir('../../')

class test_SqlConnector(TestCase):

    def setUp(self):
        self.connector = SqlConnector()

    def test_init(self):
        self.assertTrue(self.connector)
        self.assertTrue(self.connector.PGHOST)
        self.assertTrue(self.connector.PGDATABASE)

    def test_getEngine(self):
        conn = self.connector.getEngine()

    def test_loadQuery(self):
        query = "SELECT * FROM sound_type;"
        callback = self.connector.load_query(query)
        self.assertTrue(not callback.empty)
        self.assertTrue('id' in callback)
        self.assertTrue('name' in callback)

    def test_create_delete_sound_type(self):
        query = """INSERT INTO sound_type(name)
                    VALUES(%s) RETURNING id;"""
        sound_type_id = self.connector.insert_query(query, ('PERCUSSION',))
        self.assertTrue(sound_type_id)

        self.connector.delete_query('sound_type', sound_type_id)
        tmp = self.connector.load_query("SELECT * FROM sound_type WHERE id={}".format(sound_type_id))

    def test_create_(self):
        query = """INSERT INTO sound_type(name)
                            VALUES(%s) RETURNING id;"""
        sound_type_id = self.connector.insert_query(query, ('PERCUSSION',))

    def test_get_single(self):
        query = "SELECT * FROM sound_type WHERE id=1;"
        callback = self.connector.load_query(query)
        #print(callback.iloc[:1,:-1])
        #self.assertTrue(callback.iloc[:1,:])

    def test_update(self):
        values = [('name', 'INTEGRATION_TEST')]
        ans = self.connector.update_table('sound_type', 19, values)
        self.assertTrue(ans)





