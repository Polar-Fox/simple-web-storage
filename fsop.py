import os

def create_new_dir(current_user, dirpath):
    result = False
    msg = ''
    abs_path = os.path.abspath(os.path.join(current_user.get_dir(), dirpath))
    if abs_path.startswith(current_user.get_dir()):
        os.makedirs(abs_path)
        result = True
    else:
        msg = 'Trying to create incorrect folder'
    return result, msg