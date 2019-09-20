import unittest
from unittest.mock import patch
from unittest import TestCase
import os
import re

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

class TestModelRepo(TestCase):

    @patch.dict('Repositories.SampleRepository.os.environ', env_var)
    def setUp(self):
        self.repo = SampleRepository()

    def test_init(self):
        self.assertTrue(self.repo)
        self.assertEqual(os.curdir, '.')

    def test_cont(self):
        obj = self.repo.getSampleSetLocal()
        self.assertTrue(isinstance(obj, dict))
        self.assertTrue('names' in obj)
        self.assertTrue('locations' in obj)
        self.assertTrue('types' in obj)

    def test_no_hidden_files(self):
        obj = self.repo.getSampleSetLocal()

        for label in obj:
            for item in obj[label]:
                self.assertFalse(re.match(r'^\.', item))


    def test_cont(self):

        lis = self.repo.getSampleSet()
        self.assertTrue('names' in lis)









