import os, json
from flask import Flask
from flask import render_template, redirect, url_for, request,\
    send_from_directory
from flask_login import LoginManager, login_user, logout_user, current_user,\
    login_required

import conf, auth, common, fsop

common.ensure_dir(conf.media_dir)

app = Flask(__name__)
app.config["SECRET_KEY"] = "ITSASECRET"

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user = auth.User(user_id)
    return user.get()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        user = auth.User()
        if user.try_to_log_in_by_request(request):
            login_user(user)
            common.ensure_dir(user.get_dir())
            next = request.args.get('next')
            return redirect(next or url_for('index'))
        else:
            logout_user()
        print(user)
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/list/')
@app.route('/list/<path:path>')
def list(path=''):
    if not current_user.is_authenticated:
        return redirect(url_for('login', next=request.url))

    full_path = os.path.abspath(os.path.join(current_user.get_dir(), path))

    is_root = False
    if full_path == current_user.get_dir():
        is_root = True

    if full_path.startswith(current_user.get_dir()):
        if not os.path.exists(full_path):
            return 'Path not found', 404
    else:
        return redirect(url_for('list', path=''))

    if os.path.isfile(full_path):
        dirname, filename = os.path.split(full_path)
        return send_from_directory(dirname, filename)
    elif os.path.isdir(full_path):
        if not path.endswith('/') and not is_root:
            return redirect(url_for('list', path=path+'/'))
        dir_list = []
        file_list = []

        if not is_root:
            dir_list.append('..')

        for entry_name in os.listdir(full_path):
            full_entry_path = os.path.join(full_path, entry_name)
            if os.path.isfile(full_entry_path):
                file_list.append(entry_name)
            elif os.path.isdir(full_entry_path):
                dir_list.append(entry_name)

        data = {
            'dir': path,
            'dirnames': dir_list,
            'filenames': file_list
        }
        return render_template('dirlist.html', data=data)

    return 'Path not found', 404

def process_ajax_request(req, current_user):
    result = {
        'result': 'error',
        'message': ''
    }

    if 'action' in req.keys():
        if req['action'] == 'new_directory' and current_user.is_authenticated:
            op_res, msg = fsop.create_new_dir(
                current_user,
                os.path.join(req['dir'], req['dirname']))
            result = {
                'result': 'OK' if op_res else 'error',
                'message': msg
            }


    return result

@app.route('/ajax', methods=['POST'])
def ajax():
    result = {}
    if request.method == 'POST':
        print(request.url)
        result = process_ajax_request(request.form, current_user)
    return json.dumps(result)

@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login', next=request.url))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002, debug=True)
    print('\nDone.')