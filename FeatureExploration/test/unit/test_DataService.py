import unittest
from unittest.mock import patch
from unittest import TestCase
import os

from Services.DataService.DataService import DataService
from test.TestLog.TestLog import TestLog

env_var = {
    'RABBIT': 'localhost',
    'RABBIT_USER': 'guest',
    'RABBIT_PASS': 'guest',
    'GOOGLE_APPLICATION_CREDENTIALS': '/Users/vilhjamurr.vilhjalmsson/.gcp/wisebeat_bucket.json'
}

mock_locations = {
    'local': '../Data/wisebeat/raw_sound_repo/KICK/WRLD-Kick-1-D.wav',
    'GCP': ''
}

os.chdir('../../')
log = TestLog()

class test_ModelRepo(TestCase):

    @patch.dict('Repositories.RawRecordRepository.RawRecordRepo.os.environ', env_var)
    def setUp(self):
        self.service = DataService()

    def test_init(self):
        self.assertTrue(self.service)

    def test_get_records_as_pandas(self):
        frame = self.service.getRecordsAsPandas()

        log.info(frame['locations'][0])


    def test_get_records_as_pandas_local(self):
        frame = self.service.getRecordsAsPandasLocal()
        log.info(frame)

    def test_get_get_sample_local_location(self):
        rate, data = self.service.getSampleFromLocalLocation(mock_locations['local'])
        log.info(rate)
