import os

def ensure_dir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
