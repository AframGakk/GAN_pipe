from keras.layers import (Convolution2D, GlobalAveragePooling2D, BatchNormalization, Flatten,
                          GlobalMaxPool2D, MaxPool2D, concatenate, Activation, Input, Dense)
from keras.utils import Sequence, to_categorical
from keras import backend as K
from keras.activations import relu, softmax
from keras import losses, models, optimizers

class DiscriminatorModel:
    def __init__(self, config):
        nclass = 2
        self.config = config

        inp = Input(shape=(config.dim[0], config.dim[1], 1))
        x = Convolution2D(32, (4, 10), padding="same")(inp)
        x = BatchNormalization()(x)
        x = Activation("relu")(x)
        x = MaxPool2D()(x)

        x = Convolution2D(32, (4, 10), padding="same")(x)
        x = BatchNormalization()(x)
        x = Activation("relu")(x)
        x = MaxPool2D()(x)

        x = Convolution2D(32, (4, 10), padding="same")(x)
        x = BatchNormalization()(x)
        x = Activation("relu")(x)
        x = MaxPool2D()(x)

        x = Convolution2D(32, (4, 10), padding="same")(x)
        x = BatchNormalization()(x)
        x = Activation("relu")(x)
        x = MaxPool2D()(x)

        x = Flatten()(x)
        x = Dense(64)(x)
        x = BatchNormalization()(x)
        x = Activation("relu")(x)
        out = Dense(1, activation=softmax)(x)

        model = models.Model(inputs=inp, outputs=out)
        opt = optimizers.Adam(config.learning_rate)

        self.optimizers = opt
        model.compile(optimizer=opt, loss=losses.binary_crossentropy, metrics=['acc'])
        self.model = model


    def fit(self, feature_train, feature_test, target_train, target_test, verbose=1):
        return self.model.fit(feature_train, target_train, validation_data=(feature_test, target_test), batch_size=64, epochs=self.config.n_epochs, verbose=verbose)


    def predict(self, data, verbose=1):
        return self.model.predict(data, batch_size=64, verbose=verbose)