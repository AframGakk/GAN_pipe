
from Services.GanService.GanService import GanService
import traceback

def train(jobDto):

    try:
        gan = GanService(jobDto['version'],
                         jobDto['id'],
                        batch_size=jobDto['parameters']['batch_size'],
                        lrelu_alpha=jobDto['parameters']['lrelu_alpha'],
                        adam_learning_rate=jobDto['parameters']['adam_learning_rate'],
                        adam_beta1=jobDto['parameters']['adam_beta'])

        results, model_location = gan.train_old(epochs=jobDto['parameters']['episodes'])
        return results, model_location
    except Exception:
        traceback.print_exc()
        print('training failed')
        return None




