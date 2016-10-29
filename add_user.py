import sys, os
import conf, auth

if len(sys.argv) < 3:
    print('Adds a new user.')
    print('Usage: %s <username> <password>' % __file__)
    exit()

username = sys.argv[1]
password = sys.argv[2]
password_hash = auth.get_password_hash(username.encode('utf-8'), password.encode('utf-8'))

users_data = auth.get_users()

if username in users_data['users'].keys():
    print('User %s already exists.' % username)
    exit()

user_id = users_data['new_user_id']

users_data['users'][username] = {
    'id': user_id,
    'username': username,
    'password_hash': password_hash
}
users_data['user_ids'][user_id] = username
users_data['new_user_id'] = user_id + 1

auth.save_users(users_data)

print('User %s successfully added.' % username)
print('User ID: %s' % user_id)
