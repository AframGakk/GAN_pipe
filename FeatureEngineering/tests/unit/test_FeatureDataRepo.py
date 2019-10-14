from unittest import TestCase
from unittest.mock import patch
import os
import numpy as np

from repositories.FeatureDataRepo import FeatureDataRepo
from services.Log.Log import Log

os.chdir('../../')
log = Log()

env_var = {
    'GOOGLE_APPLICATION_CREDENTIALS': '/Users/vilhjamurr.vilhjalmsson/.gcp/wisebeat_bucket.json'
}

class test_FeatureDataRepo(TestCase):

    def setUp(self):
        self.repo= FeatureDataRepo()

    def test_init(self):
        self.assertTrue(self.repo)

    def test_save_local(self):
        test = np.arange(10)
        train = np.arange(5)

        self.repo.save_featuredata_local(test, train)

        self.assertTrue(os.path.isfile('../data/wisebeat/feature_data_storage/train/train.npy'))
        self.assertTrue(os.path.isfile('../data/wisebeat/feature_data_storage/test/test.npy'))

    def test_saveDataToBucket(self):
        local_file = './tmp/target_test.npy'
        version = 1
        label = 'KICK'
        bFile = 'target_test.npy'
        self.repo.saveDataToBucket(local_file, bFile, label, version)




