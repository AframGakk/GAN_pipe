import unittest
from unittest.mock import patch
from unittest import TestCase
import os
import re

from Services.DataIngestionService import DataIngestionService
from tests.TestLog.TestLog import TestLog

env_var = {
    'RABBIT': 'localhost',
    'RABBIT_USER': 'guest',
    'RABBIT_PASS': 'guest',
    'GOOGLE_APPLICATION_CREDENTIALS': '/Users/vilhjamurr.vilhjalmsson/.gcp/wisebeat_bucket.json'
}

os.chdir('../../')
log = TestLog()

class TestModelRepo(TestCase):

    @patch.dict('Repositories.SampleRepository.os.environ', env_var)
    @patch.dict('Repositories.RecordRepository.os.environ', env_var)
    def setUp(self):
        self.service = DataIngestionService()

    def test_init(self):
        self.assertTrue(self.service)

    def test_save_record_data(self):
        self.service.convertRawToRecordDataLocal()
        self.assertTrue(os.path.isfile('../Data/wisebeat/raw_data_storage/sample_records.pkl'))


    def test_conbt(self):
        self.service.convertRawToRecordData()


