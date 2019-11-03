import pickle
from google.cloud import storage

class RecordRepo:
    def __init__(self):
        self.BUCKET = storage.Client().bucket('wisebeat-raw-data-storage')

    def getRecords(self, label, version):

        self._getRecordsFromBucket(label, version)
        location = './tmp/sample_records.pkl'
        with open(location, 'rb') as file:
            data = pickle.load(file)

        return data

    def _getRecordsFromBucket(self, label, version):
        blob = self.BUCKET.blob('{}/{}/sample_records.pkl'.format(label, version))
        blob.download_to_filename('./tmp/sample_records.pkl')

    def _getRecordsLocal(self):
        location = './tmp/sample_records.pkl'
        with open(location, 'rb') as file:
            data = pickle.load(file)

        return data


