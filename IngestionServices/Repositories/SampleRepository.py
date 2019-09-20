import os
from Services.Log.Log import Log
from Repositories.BucketConnector.BucketConnector import BucketConnector

logger = Log(file_handler=True, file='./logs/logs.log')

class SampleRepository:

    def __init__(self):
        self.repo_local = '../Data/wisebeat/raw_sound_repo/'
        self.BUCKET = BucketConnector('wisebeat-raw-sound-storage').getConnection()


    def getSampleSetLocal(self):

        record_object = {
            'names': [],
            'locations': [],
            'types': []
        }

        tmp_path =  os.path.abspath(self.repo_local)

        sound_types = os.listdir(self.repo_local)

        for type in sound_types:
            if type == '.DS_Store':
                continue
            files = os.listdir(os.path.join(self.repo_local, type))
            for file in files:
                if file == '.DS_Store':
                    continue
                record_object['names'].append(file)
                record_object['locations'].append(os.path.join(os.path.join(os.path.abspath(self.repo_local), type, file)))
                record_object['types'].append(type)


        return record_object


    def getSampleSet(self):

        record_object = {
            'names': [],
            'locations': [],
            'types': []
        }

        all_blobs = self.BUCKET.list_blobs()

        for item in all_blobs:
            tmp = item.name.split('/')
            type = tmp[0]
            name = tmp[1]
            location = 'gs://wisebeat-raw-sound-storage' + '/' + item.name
            record_object['names'].append(name)
            record_object['types'].append(type)
            record_object['locations'].append(location)


        return record_object



