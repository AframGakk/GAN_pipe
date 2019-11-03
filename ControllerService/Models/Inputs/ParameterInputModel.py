
class ParameterInputModel:
    def __init__(self, batch_size, noise_dim):
        self.batch_size = batch_size
        self.noise_dim = noise_dim

    def __eq__(self, other):
        return isinstance(other, ParameterInputModel) and other.batch_size == self.batch_size and other.noise_dim== self.noise_dim

