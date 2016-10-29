import os, json
import conf

def get_password_hash(username, password):
    import hashlib
    m = hashlib.md5()
    m.update(username)
    m.update(password)
    return m.hexdigest()

def get_users():
    result = {
        'new_user_id': 1,
        'users': {}
    }
    if os.path.exists(conf.users_file):
        result = json.loads(open(conf.users_file, 'r').read())
    return result

def save_users(data):
    open(conf.users_file, 'w').write(json.dumps(data))

class User():
    def __init__(self, user_id=0):
        if isinstance(user_id, str):
            user_id = int(user_id)
        self.id = 0
        # self.try_to_log_in_by_id(user_id)

    # def try_to_log_in_by_id(self, user_id):
    #     for key, userdata in users.users.items():
    #         if userdata['id'] == user_id:
    #             self.id = user_id
    #             return
    #     self.id = 0

    def try_to_log_in_by_credentials(self, username, password):
        users_data = get_users()
        if username in users_data['users'].keys():
            user_data = users_data['users'][username]
            password_hash = get_password_hash(username.encode('utf-8'), password.encode('utf-8'))
            if user_data['password_hash'] == password_hash:
                self.id = user_data['id']
                return

        self.id = 0

    def try_to_log_in_by_request(self, req):
        username = ''
        password = ''
        for key, value in req.form.items():
            if key == 'username':
                username = value
            elif key == 'password':
                password = value
        self.try_to_log_in_by_credentials(username, password)
        if self.id > 0:
            return True
        else:
            return False

    def get_dir(self):
        if self.id > 0:
            return os.path.join(conf.media_dir, str(self.id))
        else:
            return None

    def get(self):
        if self.id > 0:
            return self
        else:
            return None

    def is_authenticated(self):
        if self.id > 0:
            return True
        else:
            return False
 
    def is_active(self):
        if self.id > 0:
            return True
        else:
            return False
 
    def is_anonymous(self):
        if self.id > 0:
            return False
        else:
            return True
 
    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User ID: %s>' % self.id