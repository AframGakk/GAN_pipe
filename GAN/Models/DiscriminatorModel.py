import numpy as np
import tensorflow as tf

from keras import losses, models, optimizers
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import (Layer, Input, Flatten, Dropout, BatchNormalization, Reshape,
                          MaxPool1D, AveragePooling1D, AveragePooling2D, GlobalAveragePooling1D, GlobalAveragePooling2D,
                          Conv2DTranspose, Conv1D, Dense, LeakyReLU, ReLU, Activation,
                          LSTM, SimpleRNNCell)


class DiscriminatorModel():
    def __init__(self):
        model = Sequential()

        model.add(Reshape((16000, 1), input_shape=(16000,)))
        model.add(Conv1D(32, 100, strides=7, padding='valid'))
        model.add(ReLU())
        model.add(AveragePooling1D(4))
        model.add(BatchNormalization(momentum=0.9))
        model.add(Dropout(rate=0.1))

        model.add(Conv1D(16, 50, strides=5, padding='valid'))
        model.add(ReLU())
        model.add(BatchNormalization(momentum=0.9))
        model.add(Dropout(rate=0.1))

        model.add(Conv1D(8, 25, strides=3, padding='valid'))
        model.add(ReLU())
        model.add(BatchNormalization(momentum=0.9))
        model.add(Dropout(rate=0.1))

        model.add(Flatten())
        model.add(Dense(1024))
        model.add(LeakyReLU(alpha=0.01))
        model.add(BatchNormalization(momentum=0.9))
        model.add(Dense(1, activation='sigmoid'))

        model.compile(loss = 'binary_crossentropy', optimizer = Adam(lr = 0.0002, beta_1 = 0.9), metrics = ['accuracy'])

        self.model = model

    def train_batch(self, real_inputs, fake_inputs):
        return self.model.train_on_batch(real_inputs, fake_inputs)


