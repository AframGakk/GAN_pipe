

class JobInputModel:
    def __init__(self, label, version, sound_type, parameters, description):
        self.label = label
        self.version = version
        self.sound_type = sound_type
        self.parameters = parameters
        self.description = description

    def __eq__(self, other):
        return isinstance(other, JobInputModel) and other.sound_type == self.sound_type and other.parameters == self.parameters

