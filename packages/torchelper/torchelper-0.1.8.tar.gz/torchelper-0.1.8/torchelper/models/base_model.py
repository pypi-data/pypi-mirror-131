import torch
import torch.nn as nn
from torchelper.utils.dist_util import get_rank
from torchelper.models.trainable import Trainable
from torch.cuda.amp import autocast, GradScaler

class BaseModel(nn.Module, Trainable):
    def __init__(self, cfg):
        super().__init__()
        self.builder = None
        self.__optimizer = None
        self.cfg = cfg
        self.is_half = cfg.get('amp', False)
        self.grad_scaler = None
        if self.is_half:
            self.grad_scaler = GradScaler()
        self.init_lr = cfg['init_lr']
        self.callbacks = []
        self.gpu_id = get_rank()
        if self.gpu_id>=0:
            self.device = torch.device('cuda:'+str(self.gpu_id))
        else:
            self.device = torch.device('cpu')


    def get_builder(self):
        return self.builder
        
    def remap_weights_name(self, weights):
        return weights

    def add_cb(self, cb):
        self.callbacks.append(cb)
    
    def perform_cb(self, event:str, *arg, **args):
        for cb in self.callbacks:
            evt_func = getattr(cb, event)
            evt_func(*arg, **args)

    def get_train_params(self):
        '''返回当前model训练参数，如果返回None，则默认为所有训练参数
        '''
        return None
    
    def get_loss(self, name:str):
        '''返回当前model loss，如果返回None，则不做梯度更新
        '''
        return None

    def get_optimizer(self):
        if self.__optimizer is None:
            params = self.get_train_params()
            if params is None:
                params = list(self.parameters())
            if len(params)>0:
                self.__optimizer = torch.optim.Adam(params, lr=self.init_lr, betas=(0.5, 0.999))
        return self.__optimizer

    def set_train(self):
        self.train()

    def set_eval(self):
        self.eval()
    # -------------------- forward -------------------- #
    def on_forward(self, epoch, step, inp):
        return self.forward(inp)
    
    # -------------------- backward -------------------- #
    def on_backward(self, epoch, step):
        if self.is_half:
            self.fp16_backward()
        else:
            self.fp32_backward()

    def fp16_backward(self):
        '''混合精度训练一个step执行反向
        '''
        with autocast():
            loss = self.get_loss()
        if loss is not None:
            optimizer = self.get_optimizer()
            if optimizer is None:
                return
            scaler = self.grad_scaler
            optimizer.zero_grad()
            # Scales loss. 为了梯度放大.
            scaler.scale(loss).backward()
            # scaler.step() 首先把梯度的值unscale回来.
            # 如果梯度的值不是 infs 或者 NaNs, 那么调用optimizer.step()来更新权重,
            # 否则，忽略step调用，从而保证权重不更新（不被破坏）
            scaler.step(optimizer)
            # 准备着，看是否要增大scaler
            scaler.update()

    def fp32_backward(self):
        '''一个step执行反向
        '''
        loss = self.get_loss()
        if loss is not None:
            optimizer = self.get_optimizer()
            if optimizer is None:
                return
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
    