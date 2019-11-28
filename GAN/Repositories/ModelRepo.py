import numpy as np
from google.cloud import storage
import os

class ModelRepo:

    def __init__(self):
        self.BUCKET = storage.Client().bucket('wisebeat-model-storage')

    def save_model_local(self, model_name, model):
        filelocation = './tmp/{}/model.h5'.format(model_name)
        model.save(filelocation)
        return filelocation

    def saveDataToBucket(self, model_name, model):
        filepath = 'models/{}/model.h5'.format(model_name)
        blob = self.BUCKET.blob(filepath)
        local_file = self.save_model_local(model_name, model)
        blob.upload_from_filename(local_file)

    def saveFigureToBucket(self, location):
        blob = self.BUCKET.blob('plots/loss_plot.png')
        blob.upload_from_filename(location)

    def saveSoundToBucket(self, location, epoch):
        blob = self.BUCKET.blob('samples/kick_{}.wav'.format(epoch))
        blob.upload_from_filename(location)

