from unittest import TestCase
import numpy as np
import os
from sklearn.preprocessing import OneHotEncoder

from Models.DiscriminatorModel import DiscriminatorModel
from Models.ModelConfig import ModelConfig

os.chdir('../../')

class test_MFCCModel(TestCase):

    def setUp(self):
        config = ModelConfig()
        self.model = DiscriminatorModel(config)

    def test_init(self):
        self.assertTrue(self.model)
        self.assertTrue(self.model.model)

    def test_fit(self):
        x_train = np.load('./tmp/KICK_1_feature_train.npy')
        x_test = np.load('./tmp/KICK_1_feature_test.npy')
        y_train = np.load('./tmp/KICK_1_target_train.npy', allow_pickle=True)
        y_test= np.load('./tmp/KICK_1_target_test.npy', allow_pickle=True)

        self.model.fit(x_train, x_test, y_train, y_test, verbose=0)


