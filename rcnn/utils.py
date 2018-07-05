import os

def get_direct_subdirs_in(dir):
    '''Returns name of subdirs'''
    if not os.path.exists(dir):
        x = next(os.walk(dir))  # Take first value only
        return x[1]
    return []

def create_dir_if_not_exists(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
