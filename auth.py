import os
import conf

users = {
    1: {
        'id': 1,
        'username': 'user1',
        'password': 'pass1',
    },
    2: {
        'id': 2,
        'username': 'user2',
        'password': 'pass2',
    },
}

class User():
    def __init__(self, user_id=0):
        if isinstance(user_id, str):
            user_id = int(user_id)
        self.id = 0
        self.try_to_log_in_by_id(user_id)

    def try_to_log_in_by_id(self, user_id):
        for key, userdata in users.items():
            if userdata['id'] == user_id:
                self.id = user_id
                return
        self.id = 0

    def try_to_log_in_by_credentials(self, username, password):
        for key, userdata in users.items():
            if userdata['username'] == username\
                and userdata['password'] == password:
                self.id = key
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