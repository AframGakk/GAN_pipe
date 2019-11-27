import numpy as np
from google.cloud import storage
import os

class SampleRepo:

    def __init__(self):
        self.BUCKET = storage.Client().bucket('wisebeat-raw-sound-storage')

    def getSoundFile(self, location):
        local_file = './tmp/samples/'+ location
        try:
            blob = self.BUCKET.blob(location)
            blob.download_to_filename(local_file)
        except Exception:
            print('Could not locate file in bucket')
            return None


