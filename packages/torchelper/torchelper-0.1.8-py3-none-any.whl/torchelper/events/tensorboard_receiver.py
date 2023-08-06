import numpy as np
from torch.utils.tensorboard import SummaryWriter
from torchelper.events.receiver import Receiver
from torchelper.events.event import Event
from torchelper.utils import logger


class TensorBoardReceiver(Receiver):
    def __init__(self, tb_dir):
        self.tb_writer = SummaryWriter(tb_dir)

    def add_scalars(self, step, metrics):
        for k, v in metrics.items():
            if v is None:
                logger.warn(k+" is None ... ")
                continue
        self.tb_writer.add_scalar(k, v, step)
        
    def add_audio(self, step, audios):
        for k, v in audios.items():
            if v is None:
                logger.warn(k+" is None ... ")
                continue    
            self.tb_writer.add_audio(k, v, step, sample_rate=16000)

    def add_images(self, step, images):
        for k, v in images.items():
            if v is None:
                logger.warn(k+" is None ... ")
                continue
            self.tb_writer.add_image(k, v, step)
        

    def on_event(self, event: Event):
        data = event.data
        extra = event.extra
        type = event.evt_type
        step = extra.get('step',None)
        if step is None:
            return
        if type==Event.Voice:
            self.add_audio(step, data)
        elif type==Event.Scalar:
            self.add_scalars(step, data)
        elif type==Event.Pic:
            self.add_images(step, data)
        else:
            logger.error("The type", type, "is not supported currently")
       
       