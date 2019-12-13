import numpy as np
import librosa
import os
import pandas

from Repositories.RecordRepo.RecordRepo import RecordRepo
from Repositories.SampleRepo.SampleRepo import SampleRepo

_recordRepo = RecordRepo()
_sampleRepo = SampleRepo()

def load_data(record_location):

    dataframe = pandas.DataFrame(_recordRepo.getRecords(record_location))

    # Get all features
    features = prepare_audiofeatures(dataframe)

    # normalize
    return normalization(features)

def prepare_audiofeatures(df):
    sampling_rate = 16000
    input_length = 64000

    features = np.empty(shape=(df.shape[0], input_length))

    placer = 0
    for i in df.index:
        _sampleRepo.getSoundFile(df['locations'][i])
        loc = os.path.join('./tmp/samples', df['locations'][i])
        data, _ = librosa.core.load(loc, sr=sampling_rate, res_type='kaiser_fast')

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


def normalization(X):
    mean = X.mean(keepdims=True)
    std = X.std(keepdims=True)
    X = (X - mean) / std
    return X



def normalize_features(features):
    mean = np.mean(features, axis=0)
    std = np.std(features, axis=0)
    feature_norm = (features - mean)/std
    return feature_norm



