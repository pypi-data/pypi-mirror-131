
from torchelper.models.trainable import Trainable
from torchelper.models.base_model import BaseModel
import torch.nn as nn
from torch.nn.parallel import DistributedDataParallel

class GroupModel(Trainable):
    def __init__(self, cfg):
        self.models = {}
        self.cfg = cfg
    
    def add_model(self, name:str, model:BaseModel):
        def get_sub_loss():
            return self.get_loss(name)
        model.get_loss = get_sub_loss
        self.models[name] = self.model_to_device(model)

    def on_backward(self, epoch, step):
        for _, model in self.models.items():
            model.module.on_backward(epoch, step)

    def model_to_device(self, net:nn.Module, find_unused_parameters=False):
        """Model to device. It also warps models with DistributedDataParallel.
        :param net: nn.Module
        """
        net = net.cuda(self.gpu_id)
        net = DistributedDataParallel(
            net, device_ids=[self.gpu_id], find_unused_parameters=find_unused_parameters)
        return net

    def forward_sub_model(self, name, data):
        return self.models[name](data)

    def set_train(self):
        for _, model in self.models.items():
            model.train()

    def set_eval(self):
        for _, model in self.models.items():
            model.eval()

    def perform_cb(self, event:str, *arg, **args):
        evt_func = getattr(self, event)
        evt_func(*arg, **args)
        for _, model in self.models.items():
            model.module.perform_cb(event, *arg, **args)

    
    