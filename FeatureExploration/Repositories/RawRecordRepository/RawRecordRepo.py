import os
import numpy as np
import pickle
import traceback

from Repositories.BucketConnector.BucketConnector import BucketConnector
from Services.Log.Log import Log

logger = Log(file_handler=True, file='./logs/logs.log')

class RawRecordRepo:

    def __init__(self):
        self.rec_repo_local = '../Data/wisebeat/raw_data_storage/'
        self.BUCKET = BucketConnector('wisebeat-raw-data-storage').getConnection()


    def getRecordData(self):

        file_path = 'all/sample_records.pkl'

        try:
            blob = self.BUCKET.blob(file_path)
            blob.download_to_filename('./tmp/sample_records.pkl')
        except Exception:
            logger.error(__name__, 'Could not locate the file {} in GCP buckets'.format(file_path))
            return None

        records = None

        try:
            with open('./tmp/sample_records.pkl', 'rb') as samplefile:
                records = pickle.load(samplefile)
        except Exception:
            logger.error(__name__, 'Could not locate the local record file after bucket download', exception=traceback.print_exc())
            pass

        return records


    def getRecordDataLocal(self):

        file_path = '../Data/wisebeat/raw_data_storage/sample_records.pkl'

        records = None

        try:
            with open(file_path, 'rb') as samplefile:
                records = pickle.load(samplefile)
        except Exception:
            logger.error(__name__, 'Could not locate the local record file after bucket download',
                         exception=traceback.print_exc())
            pass

        return records


