import unittest
from unittest.mock import patch
from unittest import TestCase
import os
import re

from Repositories.RawRecordRepository.RawRecordRepo import RawRecordRepo
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

    @patch.dict('Repositories.RawRecordRepository.RawRecordRepo.os.environ', env_var)
    def setUp(self):
        self.repo = RawRecordRepo()

    def test_init(self):
        self.assertTrue(self.repo)

    def test_get_from_buckets(self):
        records = self.repo.getRecordData()
        self.assertTrue(records is not None)
        self.assertTrue(isinstance(records, dict))

    def test_get_from_local(self):
        records = self.repo.getRecordDataLocal()
        self.assertTrue(records is not None)
        self.assertTrue(isinstance(records, dict))

