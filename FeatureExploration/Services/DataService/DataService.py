import pandas as pd

from Repositories.RawSoundRepository.RawSoundRepo import RawSoundRepo
from Repositories.RawRecordRepository.RawRecordRepo import RawRecordRepo

from Services.Log.Log import Log
soundRepo = RawSoundRepo()
recordRepo = RawRecordRepo()

logger = Log(file_handler=True, file='./logs/logs.log')

class DataService:

    def __init__(self):
        name = ''

    def getRecordsAsPandas(self):
        dataframe = pd.DataFrame(recordRepo.getRecordData())

        return dataframe

    def getRecordsAsPandasLocal(self):
        dataframe = pd.DataFrame(recordRepo.getRecordDataLocal())

        return dataframe

    def getSampleFromBucketLocation(self, location):
        rate, data = soundRepo.getFileByLocationLocal(location)
        return (rate, data)

    def getSampleFromLocalLocation(self, location):
        rate, data = soundRepo.getFileByLocationLocal(location)
        return rate, data



