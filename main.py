#!env python

# для Linux #!/usr/bin/env python3

from flask import Flask, json, request, session, url_for, redirect, render_template
from hashlib import blake2s

from wall.wall import Wall
from wall.tw_embed import twitter_embedded
from wall.config import app_secret_key, app_password_salt, app_password_hash

application = Flask(__name__)
application.config.update(
    JSON_AS_ASCII = False
)

application.secret_key = app_secret_key

################
# debug_log = True
debug_log = False
################

if debug_log: wall = Wall(True)
else: wall = Wall(False)

############################
# Pages
############################

@application.route('/')
def index():
    if '__login__' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@application.route('/login/', methods=['GET', 'POST'])
def login():
    if '__login__' not in session:
        errors = None
        if request.method == 'POST':
            r = request.form.get('password').encode('utf-8')
            pass_hash = blake2s(r, salt=app_password_salt).hexdigest()
            if pass_hash == app_password_hash:
                session.permanent = True
                session['__login__'] = "__login__"
                return redirect(url_for('index'))
            else:
                errors = True
        return render_template('login.html', errors=errors)
    return redirect(url_for('index'))

@application.route('/logout/')
def logout():
    session.pop('__login__', None)
    return redirect(url_for('login'))

############################
# API
############################

@application.route('/api/')
def api():
    if '__login__' not in session:
        return redirect(url_for('login'))
    wall.data_reset()
    wall.first()
    return json.dumps(wall.data_return())

@application.route('/api/next/')
def api_next():
    if '__login__' not in session:
        return redirect(url_for('login'))
    return json.dumps(wall.data_return())

@application.route('/api/embedded/')
def embedded():
    if '__login__' not in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        link = request.args.get('link')
        return json.dumps(twitter_embedded(link))

############################
# main()
############################

if __name__ == '__main__':
    if debug_log: application.run(debug=True)
    else: application.run(debug=False)
