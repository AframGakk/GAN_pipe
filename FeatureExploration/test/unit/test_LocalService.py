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

log = TestLog()

class test_LocalService(TestCase):

    def setUp(self):
        self.service = DataService()