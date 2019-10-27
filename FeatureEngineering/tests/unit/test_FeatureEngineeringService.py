from unittest import TestCase
from unittest.mock import patch
import os
from services.plots.plots import plot_audio

from services.FeatureEngineeringService.FeatureEngineeringService import FeatureEngineeringService
from Config.FeatureConfig import FeatureConfig
from services.Log.Log import Log
#from tests.unit.mock_returns import get_records


get_records = {
    'names': [
        'WRLD-Kick-1-D.wav',
        'WRLD-Kick-3-G.wav',
           'WRLD-Kick-5-A.wav',
           'WRLD-Kick-2-F.wav', 'WRLD-Kick-6-B.wav',
           'WRLD-Kick-4-G.wav', 'WRLDClosedHihat3.wav', 'WRLDClosedHihat2.wav', 'WRLDClosedHihat1.wav',
           'WRLDOpenHihat4.wav', 'WRLDClosedHihat 4.wav', 'WRLDOpenHihat1.wav', 'WRLDOpenHihat3.wav',
           'WRLDOpenHihat2.wav', 'WRLDSnare5-G#.wav', 'WRLDSnare2-C#.wav', 'WRLDSnare4-F.wav', 'WRLDSnare6-A.wav',
           'WRLDSnare1-C.wav', 'WRLDSnare3-D.wav', 'WRLDCrash1.wav', 'WRLDCrash2.wav', 'WRLDCrash3.wav',
           'WRLDPercussion7.wav', 'WRLDPercussion6.wav', 'WRLDPercussion4.wav', 'WRLDPercussion5.wav',
           'WRLDPercussion1.wav', 'WRLDPercussion2.wav', 'WRLDPercussion3.wav', 'WRLDClap4.wav', 'WRLDClap5.wav',
           'WRLDClap2.wav', 'WRLDClap3.wav', 'WRLDClap1.wav'], 'locations': [
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/KICK/WRLD-Kick-1-D.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/KICK/WRLD-Kick-3-G.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/KICK/WRLD-Kick-5-A.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/KICK/WRLD-Kick-2-F.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/KICK/WRLD-Kick-6-B.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/KICK/WRLD-Kick-4-G.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/HIHAT/WRLDClosedHihat3.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/HIHAT/WRLDClosedHihat2.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/HIHAT/WRLDClosedHihat1.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/HIHAT/WRLDOpenHihat4.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/HIHAT/WRLDClosedHihat 4.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/HIHAT/WRLDOpenHihat1.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/HIHAT/WRLDOpenHihat3.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/HIHAT/WRLDOpenHihat2.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/SNARE/WRLDSnare5-G#.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/SNARE/WRLDSnare2-C#.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/SNARE/WRLDSnare4-F.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/SNARE/WRLDSnare6-A.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/SNARE/WRLDSnare1-C.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/SNARE/WRLDSnare3-D.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/CRASH/WRLDCrash1.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/CRASH/WRLDCrash2.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/CRASH/WRLDCrash3.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/PERCUSSION/WRLDPercussion7.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/PERCUSSION/WRLDPercussion6.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/PERCUSSION/WRLDPercussion4.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/PERCUSSION/WRLDPercussion5.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/PERCUSSION/WRLDPercussion1.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/PERCUSSION/WRLDPercussion2.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/PERCUSSION/WRLDPercussion3.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/CLAP/WRLDClap4.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/CLAP/WRLDClap5.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/CLAP/WRLDClap2.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/CLAP/WRLDClap3.wav',
    '/Users/vilhjamurr.vilhjalmsson/Desktop/Projects/GAN_pipe/Data/wisebeat/raw_sound_repo/CLAP/WRLDClap1.wav'],
 'types': ['KICK', 'KICK', 'KICK', 'KICK', 'KICK', 'KICK', 'HIHAT', 'HIHAT', 'HIHAT', 'HIHAT', 'HIHAT', 'HIHAT',
           'HIHAT', 'HIHAT', 'SNARE', 'SNARE', 'SNARE', 'SNARE', 'SNARE', 'SNARE', 'CRASH', 'CRASH', 'CRASH',
           'PERCUSSION', 'PERCUSSION', 'PERCUSSION', 'PERCUSSION', 'PERCUSSION', 'PERCUSSION', 'PERCUSSION', 'CLAP',
           'CLAP', 'CLAP', 'CLAP', 'CLAP'
           ]
}


def getRecordsMock(self, label, version):
    return get_records


log = Log()
os.chdir('../../')

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









