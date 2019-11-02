import json

# TODO: Bæta gan_results inn í allt unitið

class JobDTO:

    def __init__(self, id, version, date_time_start, date_time_stop, model_location, sound_type, parameters):
        '''
        A data transfer object for the Job object (Training Job)
        :param id: int, The unique id.
        :param version: int, A version number.
        :param date_time_start: timestamp, when the job was created
        :param date_time_stop: timestamp, when the job finished.
        :param model_location: string, the location of the model in a model bucket.
        :param sound_type: sound_type, a sound_type entity showing the string value of a sound type.
        :param parameters: gan_parameters, entity holding all values on parameters.
        '''
        self.id = id
        self.version = version
        self.date_time_start = date_time_start
        self.date_time_stop = date_time_stop
        self.model_location = model_location
        self.sound_type = sound_type
        self.parameters = parameters


    def __eq__(self, other):
        return isinstance(other, JobDTO) and other.id == self.id

    def __hash__(self):
        return hash(self.id)

    def __dict__(self):
        return { 'id': self.id, 'version': self.version, 'date_time_start': self.date_time_start,
                 'date_time_stop': self.date_time_stop, 'model_location': self.model_location,
                 'sound_type': self.sound_type, 'parameters': self.parameters }

    def json(self):
        return json.dumps(self.__dict__())
