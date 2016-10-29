import sys, os
import conf, auth

if len(sys.argv) < 2:
    print('Removes an existing user.')
    print('Usage: %s <username>' % __file__)
    exit()

username = sys.argv[1]

users_data = auth.get_users()
if username not in users_data['users'].keys():
    print('User %s not found.' % username)
    exit()

user_id = users_data['users'][username]['id']

del users_data['users'][username]
del users_data['user_ids'][user_id]

auth.save_users(users_data)

print('User %s with ID %s successfully removed.' % (username, user_id))
print('DON\'T FORGET TO REMOVE THE USER\'S DIRECTORY!')