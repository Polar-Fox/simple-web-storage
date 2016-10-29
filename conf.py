import os

thisdir = os.path.dirname(os.path.abspath(__file__))

# Directory for users data
media_dir = os.path.join(thisdir, 'media')
# File with users
users_file = os.path.join(media_dir, 'users.json')