import numpy as np
import matplotlib.pyplot as plt

from keras.optimizers import Adam
from keras.models import Sequential
from Models.GeneratorModel import GeneratorModel
from Models.DiscriminatorModel import DiscriminatorModel
from Models.ModelConfig import ModelConfig

class GanService:
    def __init__(self):
        self.modelConfig = ModelConfig()
        self.generator = GeneratorModel()
        self.discriminator = DiscriminatorModel()
        self.stackedModel = self.stacked_model(self.generator, self.discriminator)
        self.stackedModel.compile(loss = 'binary_crossentropy', optimizer = Adam(lr = 0.0002, beta_1 = 0.9),  metrics = ['accuracy'])

        self.generatorLossHistory = []
        self.discriminatorLossHistory = []

    def train(self, epochs=500, batch = 64):

        for epoch in range(epochs):
            halfBatch = int(batch/2)
            noise = np.random.normal(0, 1, (halfBatch, 100))
            training_features = self._getFeaturesLocal('./tmp/targets.npy')

            real_inputs = training_features[np.random.randint(len(training_features), size=halfBatch),:]
            fake_inputs = self.generator.generate_sound(noise)
            x_combined_batch = np.concatenate((real_inputs, fake_inputs))
            y_combined_batch = np.concatenate((np.ones((halfBatch, 1)), np.zeros((halfBatch, 1))))
            d_loss = self.discriminator.train_batch(x_combined_batch, y_combined_batch)

            # Update stacked discriminator weights
            self.stackedModel.layers[1].set_weights(self.discriminator.model.get_weights())

            # Include discriminator loss
            d_loss_mean = np.mean(d_loss)
            self.discriminatorLossHistory.append(d_loss_mean)

            # Train stacked generator
            noise = np.random.normal(0, 1, (batch, 100))
            y_mislabled = np.ones((batch, 1))
            g_loss = self.stackedModel.train_on_batch(noise, y_mislabled)

            # Update generator Weights
            self.generator.model.set_weights(self.stackedModel.layers[0].get_weights())

            # Include generator loss
            g_loss_mean = np.mean(g_loss)
            self.generatorLossHistory.append(g_loss_mean)

            if epoch % 5 == 0:
                print("epoch: %d" % (epoch))
                print("Discriminator_loss: %f, Generator_loss: %f" % (d_loss_mean, g_loss_mean))

        self.plot_losses()



    def _getFeaturesLocal(self, location):
        with open(location, 'rb') as file:
            data = np.load(file)

        return data

    # Stacked Generator and Discriminator
    def stacked_model(self, Generator, Discriminator):
        model = Sequential()
        model.add(Generator.model)
        model.add(Discriminator.model)
        return model


    def plot_losses(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.generatorLossHistory)
        plt.plot(self.discriminatorLossHistory)
        plt.show()


    def generate_sound(self, num_to_generate):
        #seed = np.random.normal([num_to_generate, 100])
        seed = np.random.normal(0, 1, (num_to_generate, 100))
        return self.generator.generate_sound(seed)
