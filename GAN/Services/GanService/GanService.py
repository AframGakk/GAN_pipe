import numpy as np
#import matplotlib.pyplot as plt
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
    def __init__(self, record_location, version, job_id, batch_size = 64, lrelu_alpha=0.2, adam_learning_rate=0.0002, adam_beta1=0.5):
        self.batch_size = batch_size
        self.version = version
        self.job_id = job_id
        self.generator = GeneratorModel(alpha=lrelu_alpha)
        self.discriminator = DiscriminatorModel(alpha=lrelu_alpha)

        self.title='bs:{}-alpha:{}-lr:{}-beta:{}'.format(batch_size, lrelu_alpha, adam_learning_rate, adam_beta1)

        self.adverserialModel = AdverserialModel(self.discriminator.model, self.generator.model)
        self.optimizer = Adam(lr = adam_learning_rate, beta_1 = adam_beta1)

        #self.generator.model.compile(loss = 'binary_crossentropy', optimizer = self.optimizer,  metrics = ['accuracy'])
        self.discriminator.model.compile(loss = 'binary_crossentropy', optimizer = self.optimizer,  metrics = ['accuracy'])
        self.adverserialModel.model.compile(loss = 'binary_crossentropy', optimizer = self.optimizer,  metrics = ['accuracy'])

        self.training_data = load_data(record_location)

        print('====================')
        print('Training data length')
        print (len(self.training_data))
        print('====================')

        self.generatorLossHistory = []
        self.discriminatorLossHistory = []

    def train_v1(self, epochs):
        d1_hist, d2_hist, a1_hist, a2_hist, g_hist = list(), list(), list(), list(), list()
        epoch = 0
        for epoch in range(epochs):

            if len(self.training_data) < self.batch_size:
                self.batch_size = len(self.training_data)
                steps = 1
                halfBatch = self.batch_size
            else:
                halfBatch = int(self.batch_size / 2)
                steps = int(len(self.training_data) / halfBatch)


            for step in range(steps):
                # generate random real samples
                random_index = np.random.randint(0, self.training_data.shape[0] - halfBatch)
                real_inputs = self.training_data[random_index: int(random_index + halfBatch)]
                real_y = np.ones((halfBatch, 1))

                # generate fake examples
                noise = np.random.normal(-1, 1, (halfBatch, 500))
                fake_inputs = self.generator.model.predict(noise)

                x_combined_batch = np.concatenate((real_inputs, fake_inputs))
                y_combined_batch = np.concatenate((np.ones((halfBatch, 1)), np.zeros((halfBatch, 1))))

                # train discriminator
                d_loss1, d_acc1 = self.discriminator.model.train_on_batch(x_combined_batch, y_combined_batch)

                # update stacked discriminator weights
                self.adverserialModel.model.layers[1].set_weights(self.discriminator.model.get_weights())

            # Include discriminator loss & acc
            d1_hist.append(d_loss1)
            d2_hist.append(d_acc1)

            # Train stacked generator
            noise = np.random.normal(-1, 1, (self.batch_size, 500))
            y_mislabled = np.ones((self.batch_size, 1))
            g_loss, g_acc = self.adverserialModel.model.train_on_batch(noise, y_mislabled)

            # Update generator Weights
            self.generator.model.set_weights(self.adverserialModel.model.layers[0].get_weights())

            # Include generator loss
            a1_hist.append(g_loss)
            a2_hist.append(g_acc)

            if epoch % 10 == 0:
                #print("epoch: %d" % (epoch))
                print("Discriminator_loss: %f, Generator_loss: %f" % (d_loss1, g_loss))
                #self.plot_losses(epoch, bucket_save=True)
                self.model_loc = _modelRepo.saveDataToBucket('generator_{}'.format(self.title), self.generator.model, self.version, self.job_id)
                #_modelRepo.save_model_local('generator', self.generator.model)
                _modelRepo.saveDataToBucket('discriminator_{}'.format(self.title), self.generator.model, self.version, self.job_id)
                _modelRepo.saveDataToBucket('adverserial_{}'.format(self.title), self.generator.model, self.version, self.job_id)
                #first_sound = self.generate_sound(1)[0]
                #sf.write('./tmp/sample.wav', first_sound, 16000, subtype='PCM_16')
                #_modelRepo.saveSoundToBucket('./tmp/sample.wav', epoch)
                #self.plot_history_old(self.title, d1_hist, a1_hist, d2_hist, a2_hist, bucket_save=True)

            epoch += 1

        results = {
            'discriminator_loss': np.mean(d1_hist).item(),
            'generator_loss': np.mean(a1_hist).item(),
            'discriminator_accuracy': np.mean(d2_hist).item(),
            'generator_accuracy': np.mean(a2_hist).item()
        }

        return results, self.model_loc


    def train_v2(self, epochs=1000000):
        epoch = 0

        d1_hist, d2_hist, a1_hist, a2_hist, g_hist = list(), list(), list(), list(), list()

        for epoch in range(epochs):

            halfBatch = int(self.batch_size/2)
            steps = int(len(self.training_data)/halfBatch)

            for step in range(steps):
                # generate random real samples
                random_index = np.random.randint(0, self.training_data.shape[0] - halfBatch)
                real_inputs = self.training_data[random_index: int(random_index + halfBatch)]
                real_y = np.ones((halfBatch, 1))

                # update discriminator weights
                d_loss1, d_acc1 = self.discriminator.model.train_on_batch(real_inputs, real_y)

                # TODO: CHANGE
                # update stacked discriminator weights
                #self.adverserialModel.model.layers[1].set_weights(self.discriminator.model.get_weights())

                # generate fake examples
                noise = np.random.normal(-1, 1, (halfBatch, 500))
                fake_inputs = self.generator.model.predict(noise)

                # update discriminator weights
                fake_y = np.zeros((halfBatch, 1))
                d_loss2, d_acc2 = self.discriminator.model.train_on_batch(fake_inputs, fake_y)

            # prepare gan values
            noise = np.random.normal(-1, 1, (halfBatch, 500))
            y_gan = np.ones((halfBatch, 1))

            # train gan
            g_loss, g_acc = self.adverserialModel.model.train_on_batch(noise, y_gan)

            # append loss and accuracies
            d1_hist.append(d_loss1)
            d2_hist.append(d_loss2)
            g_hist.append(g_loss)
            a1_hist.append(d_acc1)
            a2_hist.append(d_acc2)

            if epoch % 2 == 0:
                #print("epoch: %d" % (epoch))
                print("Discriminator_loss: %f, Generator_loss: %f" % (d_loss1, d_loss2))
                #self.plot_losses(epoch, bucket_save=True)
                _modelRepo.saveDataToBucket('generator_{}_old'.format(self.title), self.generator.model, self.version, self.job_id)
                _modelRepo.saveDataToBucket('discriminator_{}_old'.format(self.title), self.generator.model, self.version, self.job_id)
                _modelRepo.saveDataToBucket('adverserial_{}_old'.format(self.title), self.generator.model, self.version, self.job_id)
                #first_sound = self.generate_sound(1)[0]
                #sf.write('./tmp/sample.wav', first_sound, 16000, subtype='PCM_16')
                #_modelRepo.saveSoundToBucket('./tmp/sample.wav', epoch)
                #self.plot_history(self.title, d1_hist, d2_hist, g_hist, a1_hist, a2_hist, bucket_save=True)


            epoch +=  1



    def train_v3(self, epochs):
        d1_hist, d2_hist, a1_hist, a2_hist, g_hist = list(), list(), list(), list(), list()
        epoch = 0
        for epoch in range(epochs):
            halfBatch = int(self.batch_size / 2)
            steps = int(len(self.training_data) / halfBatch)

            for step in range(steps):
                # generate random real samples
                random_index = np.random.randint(0, self.training_data.shape[0] - halfBatch)
                real_inputs = self.training_data[random_index: int(random_index + halfBatch)]
                real_y = np.ones((halfBatch, 1))

                # generate fake examples
                noise = np.random.normal(-1, 1, (halfBatch, 500))
                fake_inputs = self.generator.model.predict(noise)

                # train discriminator real input
                d_loss1, d_acc1 = self.discriminator.model.train_on_batch(real_inputs, real_y)

                # train discriminator fake input
                fake_y = np.zeros((halfBatch, 1))
                d_loss2, d_acc2 = self.discriminator.model.train_on_batch(fake_inputs, fake_y)

                # update stacked discriminator weights
                self.adverserialModel.model.layers[1].set_weights(self.discriminator.model.get_weights())


            # Train stacked generator
            noise = np.random.normal(-1, 1, (self.batch_size, 500))
            y_mislabled = np.ones((self.batch_size, 1))
            g_loss, g_acc = self.adverserialModel.model.train_on_batch(noise, y_mislabled)

            # Update generator Weights
            self.generator.model.set_weights(self.adverserialModel.model.layers[0].get_weights())

            # append loss and accuracies
            d1_hist.append(d_loss1)
            d2_hist.append(d_loss2)
            g_hist.append(g_loss)
            a1_hist.append(d_acc1)
            a2_hist.append(d_acc2)

            if epoch % 2 == 0:
                #print("epoch: %d" % (epoch))
                print("Discriminator_loss: %f, Generator_loss: %f" % (d_loss1, g_loss))
                #self.plot_losses(epoch, bucket_save=True)
                self.model_loc = _modelRepo.saveDataToBucket('generator_{}'.format(self.title), self.generator.model, self.version, self.job_id)
                #_modelRepo.save_model_local('generator', self.generator.model)
                _modelRepo.saveDataToBucket('discriminator_{}'.format(self.title), self.generator.model, self.version, self.job_id)
                _modelRepo.saveDataToBucket('adverserial_{}'.format(self.title), self.generator.model, self.version, self.job_id)
                #first_sound = self.generate_sound(1)[0]
                #sf.write('./tmp/sample.wav', first_sound, 16000, subtype='PCM_16')
                #_modelRepo.saveSoundToBucket('./tmp/sample.wav', epoch)
                #self.plot_history(self.title, d1_hist, d2_hist, g_hist, a1_hist, a2_hist, bucket_save=True)

            epoch += 1

        results = {
            'discriminator_loss': np.mean(d1_hist).item(),
            'generator_loss': np.mean(a1_hist).item(),
            'discriminator_accuracy': np.mean(d2_hist).item(),
            'generator_accuracy': np.mean(a2_hist).item()
        }

        return results, self.model_loc

'''

    def plot_history_old(self, title, d1_hist, g_hist, a1_hist, a2_hist, bucket_save=False):
        # plot loss
        plt.subplot(2, 1, 1)
        plt.plot(d1_hist, label='d-loss')
        #plt.plot(d2_hist, label='d-fake')
        plt.plot(g_hist, label='gen-loss')
        plt.legend()
        plt.title(title)
        # plot discriminator accuracy
        plt.subplot(2, 1, 2)
        plt.plot(a1_hist, label='acc-dis')
        plt.plot(a2_hist, label='acc-gen')
        plt.legend()
        # save plot to file
        #plt.savefig('./plot_line_plot_loss_old.png')
        if bucket_save:
            filename = '{}.png'.format(title)
            plt.savefig('./tmp/{}'.format(filename))
            _modelRepo.saveFigureToBucket(filename, self.version, self.job_id)
        plt.close()


    def plot_history(self, title, d1_hist, d2_hist, g_hist, a1_hist, a2_hist, bucket_save=False):
        # plot loss
        plt.subplot(2, 1, 1)
        plt.plot(d1_hist, label='d-real')
        plt.plot(d2_hist, label='d-fake')
        plt.plot(g_hist, label='gen')
        plt.legend()
        plt.title(title + '_old')
        # plot discriminator accuracy
        plt.subplot(2, 1, 2)
        plt.plot(a1_hist, label='acc-real')
        plt.plot(a2_hist, label='acc-fake')
        plt.legend()
        # save plot to file
        #plt.savefig('./plot_line_plot_loss.png')
        if bucket_save:
            filename = '{}_old.png'.format(title)
            plt.savefig('./tmp/{}'.format(filename))
            _modelRepo.saveFigureToBucket(filename, self.version, self.job_id)
        plt.close()


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

'''