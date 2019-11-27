from unittest import TestCase
import os

os.chdir('../../')
from Repositories.SampleRepo.SampleRepo import SampleRepo

class test_SampleRepo(TestCase):

    def test_get_sample(self):
        repo = SampleRepo()
        file = 'AJK Percusyn-MaxV - Kick1 1.wav'

        repo.getSoundFile(file)

        name = ''