import tensorflow as tf
from keras import layers, Sequential
from keras.layers import Dense

class GeneratorModel:
    def __init__(self):
        D = 32

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
        model.add(layers.Conv2D(1, (5, 5), padding='same'))
        model.add(layers.Activation('tanh'))

        self.model = model


    def generate_sound(self, noise, training=True):
        return self.model.predict(noise)