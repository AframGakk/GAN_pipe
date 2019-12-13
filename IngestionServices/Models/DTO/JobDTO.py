
class JobDTO:
    def __init__(self, id, label, version, date_time_start, date_time_stop, model_location, record_location, sound_type, parameters, status, results, description):
        '''
                A data transfer object for the Job object (Training Job)
                :param id: int, The unique id.
                :param label: string, name label for the job.
                :param version: int, A version number.
                :param date_time_start: timestamp, when the job was created
                :param date_time_stop: timestamp, when the job finished.
                :param model_location: string, the location of the model in a model bucket.
                :param model_location: string, the location of the record data
                :param sound_type: sound_type, a sound_type entity showing the string value of a sound type.
                :param parameters: gan_parameters, entity holding all values on parameters.
                :param status: integer, id of status in database
                :param results: entitie, result object for the results of the job
                :param description: string, description of the job
                '''
        self.id = id
        self.label = label
        self.version = version
        self.date_time_start = date_time_start
        self.date_time_stop = date_time_stop
        self.model_location = model_location
        self.record_location = record_location
        self.sound_type = sound_type
        self.parameters = parameters
        self.status = status
        self.results = results
        self.description = description

    def __dict__(self):
        return {'id': self.id, 'version': self.version, 'date_time_start': self.date_time_start,
                'date_time_stop': self.date_time_stop, 'model_location': self.model_location,
                'record_location': self.record_location, 'sound_type': self.sound_type, 'parameters': self.parameters,
                'status': self.status, 'results': self.results, 'description': self.description}