from unittest import TestCase
from unittest.mock import patch
import os
from services.plots.plots import plot_audio

from repositories.RecordRepo import RecordRepo
from services.Log.Log import Log

os.chdir('../../')
log = Log()

class test_ClientRepo(TestCase):

    #@patch.dict('repositories.ClientRepo.ClientRepo.os.environ', env_var)
    def setUp(self):
        self.repo= RecordRepo()

    def test_init(self):
        self.assertTrue(self.repo)

    def test_getRecords(self):
        label = 1
        version = 1
        data = self.repo.getRecords(label, version)



        self.assertTrue(data)
