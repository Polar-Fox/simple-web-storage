import auth

users_data = auth.get_users()

print('Users:')
print('-----------------------')
for username, data in users_data['users'].items():
	print('Username: %(username)s. ID: %(id)s' % data)
