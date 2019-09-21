import pandas as pd
import traceback

from Repositories.SampleRepository import SampleRepository
from Repositories.RecordRepository import RecordRepository
from Services.Log.Log import Log

logger = Log(file_handler=True, file='./logs/logs.log')
sampleRepo = SampleRepository()
recordRepo = RecordRepository()

class DataIngestionService:
    def __init__(self):
        self.name = ""

    def ingestAsPandas(self, data_location):
        dataset = None
        try:
            dataset = pd.read_csv(data_location).astype('float32')
            dataset.rename(columns={'0': 'label'}, inplace=True)
        except FileNotFoundError:
            logger.error(__name__, 'File could not be found, please try another location')
        except:
            logger.error(__name__, "Something happened in pulling the data to pandas", exception=traceback.print_exc())

        return dataset


    def convertRawToRecordDataLocal(self):

        bucket_obj = sampleRepo.getSampleSetLocal()
        recordRepo.saveRecordDataLocal(bucket_obj)

    def convertRawToRecordData(self):

        bucket_obj = sampleRepo.getSampleSet()
        #logger.info(__name__, bucket_obj)
        recordRepo.saveRecordData(bucket_obj)


