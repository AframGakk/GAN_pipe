import numpy as np

class ModelConfig:

    def __init__(self, n_epochs=50, n_folds=10, learning_rate=0.0001):
        self.n_epochs = n_epochs
        self.n_folds = n_folds
        self.learning_rate = learning_rate
        self.dim = (20, 32, 1)


