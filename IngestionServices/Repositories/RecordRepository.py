import os
import pickle
import traceback

from Repositories.BucketConnector.BucketConnector import BucketConnector
from Services.Log.Log import Log

logger = Log(file_handler=True, file='./logs/logs.log')

class RecordRepository:
    def __init__(self):
        self.rec_repo_local = '../Data/wisebeat/raw_data_storage/'
        self.BUCKET = BucketConnector('wisebeat-raw-data-storage').getConnection()

    def saveRecordDataLocal(self, record_data):

        abs_repo = os.path.abspath(self.rec_repo_local)
        abs_repo = abs_repo + '/'
        filename = 'sample_records.pkl'
        fileloc = abs_repo + filename

        with open(fileloc, 'wb') as file:
            pickle.dump(record_data, file)

        return fileloc


    def saveRecordData(self, record_data):
        local_file = './tmp/record_data.pkl'

        with open(local_file, 'wb') as lFile:
            pickle.dump(record_data, lFile)

        try:
            blob = self.BUCKET.blob('all/sample_records.pkl')
            blob.upload_from_filename('./tmp/record_data.pkl')
        except Exception:
            logger.error(__name__, 'Could not save record data into GCP bucket', exception=traceback.print_exc())

        os.remove('./tmp/record_data.pkl')


