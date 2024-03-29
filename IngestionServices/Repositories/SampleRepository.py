import os
from Services.Log.Log import Log
from Repositories.BucketConnector.BucketConnector import BucketConnector
import re

logger = Log(file_handler=True, file='./logs/logs.log')

class SampleRepository:

    def __init__(self):
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


    def getSampleSet(self, sound_type):

        record_object = {
            'names': [],
            'locations': [],
            'types': []
        }

        all_blobs = self.BUCKET.list_blobs()

        for item in all_blobs:
            #tmp = item.name.split('/')
            #type = tmp[0]
            #name = tmp[1]

            if not re.match(r'.*wav$', item.name):
                continue

            location = item.name
            record_object['names'].append(item.name)
            record_object['types'].append(sound_type)
            record_object['locations'].append(location)

        return record_object



