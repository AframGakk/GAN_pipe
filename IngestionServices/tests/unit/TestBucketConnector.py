import unittest
from unittest.mock import patch
from unittest import TestCase
import os

from Repositories.BucketConnector.BucketConnector import BucketConnector
from test.TestLog.TestLog import TestLog

env_var = {
    'RABBIT': 'localhost',
    'RABBIT_USER': 'guest',
    'RABBIT_PASS': 'guest',
    'GOOGLE_APPLICATION_CREDENTIALS': '/Users/vilhjamurr.vilhjalmsson/.gcp/wisebeat_bucket.json'
}

os.chdir('../../')
log = TestLog()

class TestRecordRepo(TestCase):

    @patch.dict('Repositories.BucketConnector.BucketConnector.os.environ', env_var)
    def setUp(self):
        self.bucket = BucketConnector('wisebeat-raw-data-storage').getConnection()

    def test_init(self):
        self.assertTrue(self.bucket)

    def test_cont(self):
        self.assertFalse(os.path.isfile('./tmp/record_data.pkl'))





