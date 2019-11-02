
class JobDTO:
    def __init__(self, id, version, date_time_start, date_time_stop, model_location, data_location, sound_type, parameters, status):
        self.id = id
        self.version = version
        self.date_time_start = date_time_start
        self.date_time_stop = date_time_stop
        self.model_location = model_location
        self.data_location = data_location
        self.sound_type = sound_type
        self.parameters = parameters
        self.status = status

    def __dict__(self):
        return { 'id': self.id, 'version': self.version, 'date_time_start': self.date_time_start,
                 'date_time_stop': self.date_time_stop, 'model_location': self.model_location
                 'data_location'}