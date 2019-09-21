import os
import traceback
import pickle
from scipy.io import wavfile

from Repositories.BucketConnector.BucketConnector import BucketConnector
from Services.Log.Log import Log

logger = Log(file_handler=True, file='./logs/logs.log')



class RawSoundRepo:

    def __init__(self):
        self.rec_repo_local = '../Data/wisebeat/raw_sound_repo/'
        self.BUCKET = BucketConnector('wisebeat-raw-sound-storage').getConnection()

    def getFileByLocation(self, location):

        try:
            blob = self.BUCKET.blob(location)
            splitlist = blob.name.split('/')
            filename = splitlist[len(splitlist) - 1]
            foldername = splitlist[len(splitlist) - 2]

            self.__create_sound_directory(foldername)
            full_path = os.path.join('./tmp', foldername, filename)

            blob.download_to_filename(full_path)
        except Exception:
            logger.error(__name__, 'Could not locate the file {} in GCP buckets'.format(location))
            return None

        rate = None
        data = None

        try:
            rate, data = wavfile.read(os.path.join('./tmp', foldername, filename))
        except Exception:
            logger.error(__name__, 'Could not locate file {} in the raw sound bucket'.format(filename),
                         exception=traceback.print_exc())
            pass

        return rate, data

    def getFileByLocationLocal(self, location):
        rate = None
        data = None

        try:
            rate, data = wavfile.read(location)
        except Exception:
            logger.error(__name__, 'Could not locate file in the local raw sound bucket',
                         exception=traceback.print_exc())
            pass

        return rate, data


    def __create_sound_directory(self, directory):
        if not os.path.isdir(os.path.join('./tmp', directory)):
            os.mkdir(os.path.join('./tmp', directory))


