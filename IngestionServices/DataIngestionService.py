import pandas as pd

class DataIngestionService:
    def __init__(self):
        self.name = ""

    def ingestAsPandas(self, data_location):
        dataset = None
        try:
            dataset = pd.read_csv(data_location).astype('float32')
            dataset.rename(columns={'0': 'label'}, inplace=True)
        except FileNotFoundError:
            print("File could not be found, please try another location")
        except:
            print("Something happened in pulling the data to pandas")
        return dataset