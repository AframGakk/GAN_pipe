import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf

from keras.optimizers import Adam
from keras.models import Sequential
from Models.GeneratorModel import GeneratorModel
from Models.DiscriminatorModel import DiscriminatorModel
from Models.AdverserialModel import AdverserialModel
from Models.ModelConfig import ModelConfig
from Repositories.ModelRepo import ModelRepo
from Services.FeatureEngineering.FeatureEngineering import load_data

_modelRepo = ModelRepo()

class GanService:
    def __init__(self):
        self.modelConfig = ModelConfig()
        self.generator = GeneratorModel()
        self.discriminator = DiscriminatorModel()

        self.adverserialModel = AdverserialModel(self.discriminator.model, self.generator.model)
        #self.stackedModel = self.stacked_model(self.generator.model, self.discriminator.model)

        self.optimizer = Adam(lr = 0.0002, beta_1 = 0.9)

        self.generator.model.compile(loss = 'binary_crossentropy', optimizer = self.optimizer,  metrics = ['accuracy'])
        self.discriminator.model.compile(loss = 'binary_crossentropy', optimizer = self.optimizer,  metrics = ['accuracy'])
        #self.stackedModel.compile(loss = 'binary_crossentropy', optimizer = self.optimizer,  metrics = ['accuracy'])
        self.adverserialModel.model.compile(loss = 'binary_crossentropy', optimizer = self.optimizer,  metrics = ['accuracy'])

        self.training_data = load_data(1, 1)

        self.generatorLossHistory = []
        self.discriminatorLossHistory = []

    def train(self, epochs=1000000, batch = 64):
        epoch = 0
        for epoch in range(epochs):
        #while True:
            halfBatch = int(batch/2)
            noise = np.random.normal(0, 1, (halfBatch, 100))

            random_index = np.random.randint(0, self.training_data.shape[0] - halfBatch)
            real_inputs = self.training_data[random_index: int(random_index + halfBatch)]
            #training_features = self._getFeaturesLocal('./tmp/targets.npy')

            #real_inputs = self.training_data[np.random.randint(len(self.training_data), size=halfBatch),:]
            fake_inputs = self.generator.model.predict(noise)
            x_combined_batch = np.concatenate((real_inputs, fake_inputs))
            y_combined_batch = np.concatenate((np.ones((halfBatch, 1)), np.zeros((halfBatch, 1))))
            d_loss = self.discriminator.model.train_on_batch(x_combined_batch, y_combined_batch)

            # Update stacked discriminator weights
            #self.stackedModel.layers[1].set_weights(self.discriminator.model.get_weights())
            self.adverserialModel.model.layers[1].set_weights(self.discriminator.model.get_weights())

            # Include discriminator loss
            d_loss_mean = np.mean(d_loss)
            self.discriminatorLossHistory.append(d_loss_mean)

            # Train stacked generator
            noise = np.random.normal(0, 1, (batch, 100))
            y_mislabled = np.ones((batch, 1))
            #g_loss = self.stackedModel.train_on_batch(noise, y_mislabled)
            g_loss = self.adverserialModel.model.train_on_batch(noise, y_mislabled)

            # Update generator Weights
            #self.generator.model.set_weights(self.stackedModel.layers[0].get_weights())
            self.generator.model.set_weights(self.adverserialModel.model.layers[0].get_weights())

            # Include generator loss
            g_loss_mean = np.mean(g_loss)
            self.generatorLossHistory.append(g_loss_mean)

            if epoch % 100 == 0:
                print("epoch: %d" % (epoch))
                print("Discriminator_loss: %f, Generator_loss: %f" % (d_loss_mean, g_loss_mean))
                self.plot_losses(epoch, bucket_save=True)
                _modelRepo.saveDataToBucket('generator', self.generator.model)
                _modelRepo.saveDataToBucket('discriminator', self.generator.model)
                _modelRepo.saveDataToBucket('adverserial', self.generator.model)
                #first_sound = self.generate_sound(1)[0]
                #sf.write('./tmp/sample.wav', first_sound, 16000, subtype='PCM_16')
                #_modelRepo.saveSoundToBucket('./tmp/sample.wav', epoch)

            epoch +=  1

        #self.plot_losses()



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


    def plot_losses(self, epoch, bucket_save=False):
        plt.figure(figsize=(10, 5))
        plt.plot(self.generatorLossHistory)
        plt.plot(self.discriminatorLossHistory)
        plt.title('Epoch {}'.format(epoch))
        plt.ylabel('Loss')
        plt.xlabel('Epochs')
        if bucket_save:
            plt.savefig('./tmp/loss_plot.png')
            _modelRepo.saveFigureToBucket('./tmp/loss_plot.png')
            return

        plt.show()


    def generate_sound(self, num_to_generate):
        #seed = np.random.normal([num_to_generate, 100])
        seed = np.random.normal(0, 1, (num_to_generate, 100))
        return self.generator.model.predict(seed)

