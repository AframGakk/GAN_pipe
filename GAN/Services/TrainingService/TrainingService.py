from Services.GanService.GanService import GanService


def train(info_obj):
    _ganService = GanService(info_obj['record_location'],
                             info_obj['version'],
                             info_obj['id'],
                             info_obj['parameters']['batch_size'],
                             info_obj['parameters']['lrelu_alpha'],
                             info_obj['parameters']['adam_learning_rate'],
                             info_obj['parameters']['adam_beta'])
    return _ganService.train_v1(info_obj['parameters']['episodes'])

