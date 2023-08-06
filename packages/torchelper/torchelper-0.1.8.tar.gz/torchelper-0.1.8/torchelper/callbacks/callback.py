
class Callback():
    def __init__(self):
        pass

    def on_begin_train(self, epoch:int):
        pass

    def on_end_train(self):
        pass


    def on_begin_epoch(self, epoch:int):
        pass

    def on_end_epoch(self, epoch:int):
        pass


    def on_begin_step(self, epoch:int, step:int):
        pass

    def on_end_step(self, epoch:int, step:int):
        pass
    

    def on_begin_val(self, epoch:int):
        pass
    
    def on_val(self, epoch:int, data):
        pass

    def on_end_val(self, epoch:int, metric_dict:dict):
        pass

  