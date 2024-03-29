

class JobInputModel:
    def __init__(self, version, sound_type, parameters):
        self.version = version
        self.sound_type = sound_type
        self.parameters = parameters

    def __eq__(self, other):
        return isinstance(other, JobInputModel) and other.sound_type == self.sound_type and other.parameters == self.parameters

