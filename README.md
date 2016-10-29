# SimpleWebStorage

This is a very simple web file sharing application. It can be used for sharing files with another people (by giving them
a public link) or just as your private online storage.

SimpleWebStorage provides simple authorization and user management.

User management works via the command line. Users manage their files via the web interface.

## Usage

Each user has their own file storage directory. A user can manage files and folders in their storage directory
(create/rename/delete subdirectories, upload/rename/delete files) and make/remove public links to files via the web
interface.

## Prerequisites

- Python 3
- Flask
- Flask-Login

```
pip install flask
pip install flask-login
```

## User management

All the info about users is stored in a JSON-file.

User management functionality is provided by several auxiliary scripts.

### Adding a user

```add_user.py <username> <password>```

### Deleting a user

```remove_user.py <username>```

### List users

```list_users.py```


## Configuration

All the configuration is in ```conf.py``` file:

- *conf.media_dir* -- storage directory
- *conf.users_file* -- JSON-file with info about users. It's created and managed by user management scripts.