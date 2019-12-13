import pickle
from google.cloud import storage

class RecordRepo:
    def __init__(self):
        self.BUCKET = storage.Client().bucket('wisebeat-raw-data-storage')

    def getRecords(self, location):

        self._getRecordsFromBucket(location)
        location = './tmp/sample_records.pkl'
        with open(location, 'rb') as file:
            data = pickle.load(file)

        return data

    def _getRecordsFromBucket(self, location):
        blob = self.BUCKET.blob(location)
        blob.download_to_filename('./tmp/sample_records.pkl')

    def _getRecordsLocal(self):
        location = './tmp/sample_records.pkl'
        with open(location, 'rb') as file:
            data = pickle.load(file)

        return data


