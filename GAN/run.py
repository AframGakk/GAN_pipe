from Services.GanService.GanService import GanService

# Run hyperparameter tuning
def hyperparameter_tuning():
    hyperparams = {
        'adam_learning_rate': [ 0.002, 0.02, 0.2 ],
        'adam_beta_1': [0.25, 0.5, 0.75],
        'lrelu_alpha': [ 0.01, 0.1, 0.2 ],
        'batch_size': [ 32, 64, 128 ]
    }

    epochs = 1000

    for lr_item in hyperparams['adam_learning_rate']:
        for beta_item in hyperparams['adam_beta_1']:
            for alpha in hyperparams['lrelu_alpha']:
                for batch_size in hyperparams['batch_size']:
                    _service = GanService('ronja_v2', 1, batch_size=batch_size, lrelu_alpha=alpha, adam_learning_rate=lr_item, adam_beta1=beta_item)
                    _service.train_old(epochs=epochs)
                    _service.train(epochs=epochs)

def train():
    epochs = 1
    version = 'ronja_v2'
    id = 1
    batch = 128
    alpha = 0.1
    lr = 0.002
    beta = 0.75

    gan = GanService(version,
                     id,
                     batch_size=batch,
                     lrelu_alpha=alpha,
                     adam_learning_rate=lr,
                     adam_beta1=beta)

    gan.train_old(epochs=epochs)


train()






