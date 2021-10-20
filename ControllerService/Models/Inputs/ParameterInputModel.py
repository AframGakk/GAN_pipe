
class ParameterInputModel:
    def __init__(self, batch_size, learning_rate, beta, alpha, episodes):
        self.batch_size = batch_size
        self.adam_learning_rate = learning_rate
        self.adam_beta = beta
        self.lrelu_alpha = alpha
        self.episodes = episodes


    def __eq__(self, other):
        return isinstance(other, ParameterInputModel) and other.batch_size == self.batch_size and other.noise_dim== self.noise_dim

