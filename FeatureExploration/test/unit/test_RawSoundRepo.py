import unittest
from unittest.mock import patch
from unittest import TestCase
import os

from Repositories.RawSoundRepository.RawSoundRepo import RawSoundRepo
from test.TestLog.TestLog import TestLog

env_var = {
    'RABBIT': 'localhost',
    'RABBIT_USER': 'guest',
    'RABBIT_PASS': 'guest',
    'GOOGLE_APPLICATION_CREDENTIALS': '/Users/vilhjamurr.vilhjalmsson/.gcp/wisebeat_bucket.json'
}

mock_locations = {
    'local': '../Data/wisebeat/raw_sound_repo/KICK/WRLD-Kick-1-D.wav',
    'GCP': 'KICK/WRLD-Kick-1-D.wav'
}

os.chdir('../../')
log = TestLog()

class test_ModelRepo(TestCase):

    @patch.dict('Repositories.RawRecordRepository.RawRecordRepo.os.environ', env_var)
    def setUp(self):
        self.repo = RawSoundRepo()

    def test_init(self):
        self.assertTrue(self.repo)

    def test_get_by_location(self):

        rate, data = self.repo.getFileByLocation(mock_locations['GCP'])
        log.info(rate)

    def test_get_by_location_local(self):
        rate, data = self.repo.getFileByLocationLocal(mock_locations['local'])
        log.info(rate)


