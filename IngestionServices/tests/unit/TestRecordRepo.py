import unittest
from unittest.mock import patch
from unittest import TestCase
import os

from Repositories.RecordRepository import RecordRepository
from Repositories.SampleRepository import SampleRepository
from tests.TestLog.TestLog import TestLog

env_var = {
    'RABBIT': 'localhost',
    'RABBIT_USER': 'guest',
    'RABBIT_PASS': 'guest',
    'GOOGLE_APPLICATION_CREDENTIALS': '/Users/vilhjamurr.vilhjalmsson/.gcp/wisebeat_bucket.json'
}

os.chdir('../../')
log = TestLog()

class TestRecordRepo(TestCase):

    @patch.dict('Repositories.RecordRepository.os.environ', env_var)
    def setUp(self):
        self.repo = RecordRepository()

    def test_init(self):
        self.assertTrue(self.repo)
        self.assertEqual(os.curdir, '.')

    def test_saves_records_locally(self):
        sampleRepo = SampleRepository()
        record_data = sampleRepo.getSampleSetLocal()

        loc = self.repo.saveRecordDataLocal(record_data)
        self.assertTrue(os.path.isfile(loc))

    def test_cont(self):
        sampleRepo = SampleRepository()
        record_data = sampleRepo.getSampleSet()
        log.info(record_data)
        self.repo.saveRecordData(record_data)
