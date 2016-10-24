from flask import Flask
from flask import render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, current_user,\
    login_required

import conf, auth, common

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

@app.route('/list/<path:path>')
def list(path):
    if not current_user.is_authenticated:
        return redirect(url_for('login', next=request.url))
    return path

@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login', next=request.url))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002, debug=True)
    print('\nDone.')