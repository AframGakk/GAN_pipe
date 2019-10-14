from unittest import TestCase
from unittest.mock import patch
import os
from services.plots.plots import plot_audio

from services.FeatureEngineeringService.FeatureEngineeringService import FeatureEngineeringService
from Config.FeatureConfig import FeatureConfig
from services.Log.Log import Log
from tests.unit.mock_returns import get_records

def getRecordsMock(self, label, version):
    return get_records

os.chdir('../../')
log = Log()

class test_ClientRepo(TestCase):

    @patch('repositories.RecordRepo.RecordRepo.getRecords', getRecordsMock)
    def setUp(self):
        self.service = FeatureEngineeringService()


    def test_init(self):
        self.assertTrue(self.service)


    def test_get_local_record(self):
        label = 'KICK'
        version = 1
        frame = self.service.getRecordDataframe(label, version)
        self.assertTrue('types' in frame)
        self.assertTrue('locations' in frame)
        self.assertTrue('names' in frame)


    def test_prepare_audiofeatures(self):
        config = FeatureConfig()
        label = 'KICK'
        version = 1
        dataframe = self.service.getRecordDataframe(label, version)
        features = self.service.prepare_audiofeatures(dataframe, config)
        self.assertEqual(dataframe.shape[0], len(features))


    def test_prepare_targetlabels(self):
        label = 'KICK'
        version = 1
        dataframe = self.service.getRecordDataframe(label, version)
        undersampled = self.service._undersampling(dataframe, label)

        lDf = self.service.prepare_targetlabels(undersampled, label)

        self.assertEqual(len(lDf), len(undersampled))
        self.assertLess(lDf[0], 2)


    def test_normalizing_features(self):
        config = FeatureConfig()
        label = 'KICK'
        version = 1
        dataframe = self.service.getRecordDataframe(label, version)
        features = self.service.prepare_audiofeatures(dataframe, config)
        norm_feat = self.service._normalize_features(features)

        self.assertEqual(len(features), len(norm_feat))


    def test_undersampling(self):
        '''
        should return a new dataframe with 50% KICK data and rest an equal mix of others.
        :return:
        '''
        label = 'KICK'
        version = 1
        dataframe = self.service.getRecordDataframe(label, version)
        undersampled = self.service._undersampling(dataframe, label)
        self.assertAlmostEqual(undersampled[undersampled['types'] == label].shape[0], undersampled[undersampled['types'] != label].shape[0])

    def test_train_test_split(self):
        label = 'KICK'
        version = 1
        dataframe = self.service.getRecordDataframe(label, version)
        undersampled = self.service._undersampling(dataframe, label)

        features = undersampled.iloc[:,:-1]
        targets = self.service.prepare_targetlabels(undersampled, label)

        feat_train, feat_test, targ_train, targ_test = self.service._train_test_split(features, targets)

        self.assertEqual(len(feat_train), len(targ_train))
        self.assertEqual(len(feat_test), len(targ_test))


    def test_transform_features(self):
        label = 'KICK'
        version = 1

        self.service.transformFeatures(label, version)

        self.assertTrue(os.path.isfile('./tmp/feature_train.npy'))
        self.assertTrue(os.path.isfile('./tmp/feature_test.npy'))
        self.assertTrue(os.path.isfile('./tmp/target_train.npy'))
        self.assertTrue(os.path.isfile('./tmp/target_test.npy'))









