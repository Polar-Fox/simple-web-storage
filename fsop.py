import os, uuid, json, shutil
import conf

def ensure_dir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

def get_dir_options(path):
    result = {}

    opts_filepath = os.path.join(path, '.options')

    if os.path.exists(opts_filepath):
        result = json.loads(open(opts_filepath, 'r').read())

    return result

def set_dir_options(path, opts):
    result = {}

    opts_filepath = os.path.join(path, '.options')

    open(opts_filepath, 'w').write(json.dumps(opts))

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

def make_public_link(current_user, dirname, filename):
    abs_path = os.path.abspath(os.path.join(current_user.get_dir(), dirname, filename))
    if abs_path.startswith(current_user.get_dir()):
        if os.path.exists(abs_path):
            file_uuid = uuid.uuid4().hex
            filepath = abs_path[len(conf.media_dir):].strip('\\').strip('/')
            public_link = os.path.join(file_uuid, filename).replace('\\', '/')
            public_dir = os.path.join(conf.media_dir, 'public')
            ensure_dir(public_dir)
            open(os.path.join(public_dir, file_uuid), 'wb').write(filepath.encode('utf-8'))
            dir_options = get_dir_options(os.path.dirname(abs_path))
            if 'public_files' not in dir_options.keys():
                dir_options['public_files'] = {}
            dir_options['public_files'][filename] = file_uuid
            set_dir_options(os.path.dirname(abs_path), dir_options)
    return True, ''

def remove_public_link(current_user, dirname, filename, force=False):
    abs_path = os.path.abspath(os.path.join(current_user.get_dir(), dirname, filename))
    if abs_path.startswith(current_user.get_dir()):
        if os.path.exists(abs_path) or force:
            dir_options = get_dir_options(os.path.dirname(abs_path))
            if 'public_files' in dir_options.keys():
                if filename in dir_options['public_files'].keys():
                    file_uuid = dir_options['public_files'][filename]
                    del dir_options['public_files'][filename]
                    set_dir_options(os.path.dirname(abs_path), dir_options)

                    public_dir = os.path.join(conf.media_dir, 'public')
                    public_uuid_filepath = os.path.join(public_dir, file_uuid)
                    if os.path.exists(public_uuid_filepath):
                        os.remove(public_uuid_filepath)
            
    return True, ''

def rename_entry(current_user, dirname, old_name, new_name):
    old_abs_path = os.path.abspath(os.path.join(current_user.get_dir(), dirname, old_name))
    new_abs_path = os.path.abspath(os.path.join(current_user.get_dir(), dirname, new_name))
    if old_abs_path.startswith(current_user.get_dir()):
        if os.path.exists(old_abs_path):
            os.rename(old_abs_path, new_abs_path)
            remove_public_link(current_user, dirname, old_name, force=True)
            
    return True, ''

def delete_entry(current_user, dirname, entryname):
    abs_path = os.path.abspath(os.path.join(current_user.get_dir(), dirname, entryname))
    if abs_path.startswith(current_user.get_dir()):
        if os.path.exists(abs_path):
            remove_public_link(current_user, dirname, entryname)
            if os.path.isfile(abs_path):
                os.remove(abs_path)
            elif os.path.isdir(abs_path):
                shutil.rmtree(abs_path)

    return True, ''