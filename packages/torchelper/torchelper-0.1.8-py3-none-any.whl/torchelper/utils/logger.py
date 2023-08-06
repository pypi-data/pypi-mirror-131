
from .dist_util import master_only
import functools
import time
from termcolor import colored
 
__log_file=None


def __my_log(level:int, *args):
    log = [str(v) for v in args]
    now = time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())
    log = now + ' '.join(log)
    if level==0:
        print(log)
    elif level == 1:
        print(colored(log, 'yellow'))
    else:
        print(colored(log, 'red'))
    if __log_file is not None:
        __log_file.write(log+"\n")

@master_only
def debug(*msg):
    __my_log(0, *msg)

@master_only
def log(*msg):
    __my_log(0, *msg)

@master_only
def warn(*msg):
    __my_log(1, *msg)

@master_only
def error(*msg):
    __my_log(2, *msg)

  
@master_only
def init_log(log_file_path=None):

    global __log_file
    __log_file = open(log_file_path, "w+",encoding="utf-8")
 