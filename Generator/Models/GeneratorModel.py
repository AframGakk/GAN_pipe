from keras.optimizers import Adam

from keras.models import Sequential
from keras.layers import (Layer, Input, Flatten, Dropout, BatchNormalization, Reshape,
                          MaxPool1D, AveragePooling1D, AveragePooling2D, GlobalAveragePooling1D, GlobalAveragePooling2D,
                          Conv2DTranspose, Conv1D, Dense, LeakyReLU, ReLU, Activation,
                          LSTM, SimpleRNNCell)

class GeneratorModel:
    def __init__(self):

        model = Sequential()
        model.add(Dense(1000, input_shape=(100,)))
        model.add(LeakyReLU(alpha=0.01))
        model.add(BatchNormalization(momentum=0.9))
        model.add(Reshape((1000, 1)))

        model.add(Conv1D(4, 25, padding='same'))
        model.add(ReLU())
        model.add(BatchNormalization(momentum=0.9))
        model.add(Dropout(rate=0.1))

        model.add(Conv1D(8, 50, padding='same'))
        model.add(ReLU())
        model.add(BatchNormalization(momentum=0.9))
        model.add(Dropout(rate=0.1))

        model.add(Conv1D(16, 100, padding='same'))
        model.add(Dropout(rate=0.3))
        model.add(Flatten())

        model.compile(loss = 'binary_crossentropy', optimizer = Adam(lr = 0.0002, beta_1 = 0.9), metrics =['accuracy'])

        self.model = model


    def generate_sound(self, noise, training=True):
        return self.model.predict(noise)
        #self.model.





# OLD MODEL
'''
model = Sequential()

        model.add(Dense(256 * D, input_dim=100))
        model.add(layers.Reshape((4, 4, 16 * D)))
        model.add(layers.Activation('relu'))

        model.add(layers.UpSampling2D(size=(2, 2)))
        model.add(layers.Conv2D(8 * D, (5, 5), padding='same'))
        model.add(layers.Activation('relu'))

        model.add(layers.UpSampling2D(size=(2, 2)))
        model.add(layers.Conv2D(4 * D, (5, 5), padding='same'))
        model.add(layers.Activation('relu'))

        model.add(layers.UpSampling2D(size=(2, 2)))
        model.add(layers.Conv2D(2 * D, (5, 5), padding='same'))
        model.add(layers.Activation('relu'))
        model.add(layers.Conv2D(D, (5, 5), padding='same'))

        model.add(layers.UpSampling2D(size=(2, 2)))
        model.add(layers.Activation('relu'))

        model.add(layers.UpSampling2D(size=(2, 2)))
        model.add(layers.Conv2D(2, (5, 5), padding='same'))
        model.add(layers.Activation('tanh'))

'''