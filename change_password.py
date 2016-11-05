import sys, os
import conf, auth

if len(sys.argv) < 3:
    print('Changes user password.')
    print('Usage: %s <username> <new_password>' % __file__)
    exit()

username = sys.argv[1]
password = sys.argv[2]

users_data = auth.get_users()
if username not in users_data['users'].keys():
    print('User %s not found.' % username)
    exit()

user_id = users_data['users'][username]['id']

password_hash = auth.get_password_hash(username.encode('utf-8'), password.encode('utf-8'))
users_data['users'][username]['password_hash'] = password_hash

auth.save_users(users_data)

print('Password for user %s successfully changed.' % username)
print('User ID: %s' % user_id)
