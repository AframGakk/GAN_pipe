import numpy as np

class FeatureConfig(object):
    def __init__(self, sampling_rate=16000, audio_duration=1, mfcc_mels=20):
        self.sampling_rate = sampling_rate
        self.audio_duration = audio_duration
        self.mfcc_mels = mfcc_mels
        self.sample_length = self.sampling_rate * self.audio_duration
        self.sample_dimension = (self.mfcc_mels, 1 + int(np.floor(self.sample_length/512)), 1)