import os
from google.cloud import storage

class BucketConnector:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.BUCKET = storage.Client().bucket(bucket_name)

    def getConnection(self):
        return self.BUCKET


