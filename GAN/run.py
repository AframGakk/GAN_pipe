from Services.GanService import GanService

_service = GanService()
_service.train_old(epochs=1000000, batch=64)


