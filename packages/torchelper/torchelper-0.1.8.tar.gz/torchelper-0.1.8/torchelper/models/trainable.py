
from torchelper.callbacks.callback import Callback


class Trainable(Callback):
    '''可训练的抽象类
    '''
    def __init__(self):
        pass

 
    def get_loss(self, name:str):
        '''返回当前model loss，如果返回None，则不做梯度更新
        '''
        return None

    def set_train(self):
        pass

    def set_eval(self):
        pass
    
      
   
    def on_begin_forward(self, data, epoch, step):
        None

    def on_forward(self,  epoch, step, inp):
        return None
    
    def on_end_forward(self,  epoch, step):
        return None
    
    def on_begin_backward(self,  epoch, step):
        return None

    def on_backward(self,  epoch, step):
        return None
    
    def on_end_backward(self, epoch, step):
        return None