from torchelper.utils.dist_util import get_rank
from torchelper.events.receiver import Receiver
from torchelper.events.event import Event
from tqdm import tqdm


class PBar(Receiver):
    def __init__(self, iter):
        rank = get_rank()
        self.is_master = rank == 0
        if self.is_master:
            self.bar = tqdm(iter)
        else:
            self.bar = iter

    def __iter__(self):
        return self.bar.__iter__()
    
    def on_event(self, event: Event):
        if not self.is_master:
            return
        if event.evt_type == Event.Scalar:
            data = event.data
            msg = []
            for k, v in data.items():
                msg.append('%s:%.5f'%(k, v))
            self.bar.set_description(', '.join(msg))
