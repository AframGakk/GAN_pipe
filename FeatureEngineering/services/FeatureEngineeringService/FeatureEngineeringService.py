import pandas as pd
import numpy as np
import librosa
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import os

from repositories.RecordRepo import RecordRepo
from repositories.FeatureDataRepo import FeatureDataRepo
from repositories.SampleRepo import SampleRepo
from Config.FeatureConfig import FeatureConfig

class FeatureEngineeringService:
    def __init__(self):
        self._recordRepo = RecordRepo()
        self._featureRepo = FeatureDataRepo()
        self._sampleRepo = SampleRepo()
        self.LOCAL = True

    def getRecordDataframe(self, label, version):
        dataframe = self._recordRepo.getRecords(label, version)

        return pd.DataFrame(dataframe)

    def transformFeatures(self, label, version):
        config = FeatureConfig()

        # Get the dataframe
        dataframe = self.getRecordDataframe(label, version)

        # Get all features
        features = self.prepare_audiofeatures(dataframe, config)

        # Normalize
        #features_norm = self._normalize_features(features)

        # Save locally
        self._save_numpy_local(features, 'features')

        # Save in bucket
        self._moveFilesToBucket(label, version)

        # Clean up tmp folder
        self._cleanup_tmp()


    def prepare_audiofeatures(self, df, config):
        features = np.empty(shape=(df.shape[0], config.sampling_rate))
        input_length = config.sample_length

        placer = 0
        for i in df.index:
            self._getRawSoundFile(df['locations'][i])
            loc = os.path.join('./tmp/', df['locations'][i])
            data, _ = librosa.core.load(loc, sr=config.sampling_rate, res_type='kaiser_fast')

            if len(data) > input_length:
                data = data[:input_length]
            else:
                if input_length > len(data):
                    max_offset = input_length - len(data)
                else:
                    offset = 0
                data = np.pad(data, (0, max_offset), "constant")

            features[placer,] = data
            placer = placer + 1

        return features


    def transformFeatures_MFCC(self, label, version):

        # Get the dataframe
        dataframe = self.getRecordDataframe(label, version)

        # undersample
        undersampled = self._undersampling(dataframe, label)

        # split features and labels
        features = undersampled.iloc[:,:-1]
        targets = self.prepare_targetlabels_MFCC(undersampled, label)

        # split test and train
        feature_train, feature_test, target_train, target_test = self._train_test_split(features, targets)

        # prepare audio features
        m_config = FeatureConfig()
        feature_train = self.prepare_audiofeatures_MFCC(feature_train, m_config)
        feature_test = self.prepare_audiofeatures_MFCC(feature_test, m_config)

        # normalize audio features
        feature_train = self._normalize_features(feature_train)
        feature_test = self._normalize_features(feature_test)

        # save files locally
        self._save_numpy_local(target_train.to_numpy(), 'target_train')
        self._save_numpy_local(target_test.to_numpy(), 'target_test')
        self._save_numpy_local(feature_train, 'feature_train')
        self._save_numpy_local(feature_test, 'feature_test')


    def prepare_audiofeatures_MFCC(self, df, mfcc_config):
        features = np.empty(shape=(df.shape[0], mfcc_config.sample_dimension[0], mfcc_config.sample_dimension[1], 1))
        input_length = mfcc_config.sample_length

        placer = 0
        for i in df.index:
            data, _ = librosa.core.load(df['locations'][i], sr=mfcc_config.sampling_rate, res_type='kaiser_fast')

            if len(data) > input_length:
                max_offset = len(data) - input_length
                offset = np.random.randint(max_offset)
                data = data[offset:(input_length + offset)]
            else:
                if input_length > len(data):
                    max_offset = input_length - len(data)
                    offset = np.random.randint(max_offset)
                else:
                    offset = 0
                data = np.pad(data, (offset, input_length - len(data) - offset), "constant")

            data = librosa.feature.mfcc(data, sr=mfcc_config.sampling_rate, n_mfcc=mfcc_config.mfcc_mels)
            data = np.expand_dims(data, axis=-1)
            features[placer,] = data
            placer = placer + 1

        return features

    def _getRawSoundFile(self, location):
        self._sampleRepo.getSoundFile(location)

    def prepare_targetlabels_MFCC(self, df, true_label):
        '''
        # label encoder
        #le = LabelEncoder()
        #label_targets = le.fit_transform(df['types'])
        #unique_labels = np.unique(label_targets)

        #labels = df.iloc[:,2]
        # one hot encoder
        #oh = OneHotEncoder()
        #oh_labels = oh.fit_transform(label_targets).toarray()

        onehot = pd.get_dummies(df['types'])
        target_labels = onehot.columns
        labels = onehot.as_matrix()

        test_kick = onehot['KICK'].as_matrix()

        self._save_encoder(onehot)
        '''

        df.loc[df.types != true_label, 'types'] = 0
        df.loc[df.types == true_label, 'types'] = 1
        targets = df.iloc[:,2]

        return targets


    def _normalize_features(self, features):
        mean = np.mean(features, axis=0)
        std = np.std(features, axis=0)
        feature_norm = (features - mean)/std

        mean_all = mean['mean']

        return feature_norm


    def _train_test_split(self, features, targets, split=0.2):
        return train_test_split(features, targets, test_size=split, random_state=42)


    def _undersampling(self, dataframe, label):
        df_labelled = dataframe[dataframe['types'] == label]
        df_labelled_count = df_labelled.shape[0]
        df_rand = dataframe[dataframe['types'] != label]

        df_under = df_rand.sample(df_labelled_count)
        df_comined = pd.concat([df_labelled, df_under], axis=0)
        df = shuffle(df_comined)
        return df

    def _save_numpy_local(self, data, filename):
        local_dir = './tmp/'
        file = local_dir + filename
        np.save(file, data)

    def _moveFilesToBucket(self, label, version):
        self._featureRepo.saveDataToBucket('./tmp/features.npy' , 'features.npy', label, version)

    def _moveFilesToBucket_MFCC(self, label, version):
        filenames = ['feature_train.npy', 'feature_test.npy', 'target_train.npy', 'target_test.npy']
        for file in filenames:
            self._featureRepo.saveDataToBucket('./tmp/{}'.format(file), file, label, version)

    def _cleanup_tmp(self):
        file_list = os.listdir('./tmp')

        for file in file_list:
            os.remove(os.path.join('./tmp', file))





