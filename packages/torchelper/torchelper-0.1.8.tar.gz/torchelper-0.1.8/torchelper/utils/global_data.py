

__global_data = {}

def set_global(key:str, data):
    __global_data[key] = data

def get_global(key, dft=None):
    return __global_data.get(key, dft)