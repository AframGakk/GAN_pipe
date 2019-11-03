import numpy as np
from google.cloud import storage
import os

class FeatureDataRepo:

    def __init__(self):
        self.BUCKET = storage.Client().bucket('wisebeat-feature-storage')

    def save_featuredata_local(self, train, test):
        repo_dir = './tmp/'
        train_file = repo_dir + 'train/train'
        test_file = repo_dir + 'test/test'

        np.save(train_file, train)
        np.save(test_file, test)

    def saveDataToBucket(self, local_file, bFilename, label, version):
        filepath = '{}/{}/{}'.format(label, version, bFilename)
        blob = self.BUCKET.blob(filepath)
        blob.upload_from_filename(local_file)




