import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# register a new user
# if succesful redirect to login
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        # get values from forms
        firstname = request.form['firstname']
        username = request.form['username']
        password = request.form['password']
        goalweight = request.form['goalweight']

        # load database
        db = get_db()
        error = None #track errors

        # check froms are not empty
        if not firstname:
            error = 'First name is required.'
        elif not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not goalweight:
            error = 'Goal Weight is required.'
        # check username does not exist
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        # no errors insert into database and redirect to login page
        if error is None:
            db.execute(
                'INSERT INTO user (firstname, username, password, goalweight) VALUES (?, ?, ?, ?)',
                (firstname, username, generate_password_hash(password), goalweight)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

# user login
# return the user login template
@bp.route('/login', methods=('GET', 'POST'))
def login():

    # get username and password
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        # check username and password against file
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        # no errors update session id with user id
        # run url in blog.py file user route
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            # return redirect(url_for('blog.user', id=user['id']))
            return redirect(url_for('blog.get_user_posts'))

        flash(error)

    return render_template('auth/login.html')

# update g.user
@bp.before_app_request
def load_logged_in_user():
    # get session id
    user_id = session.get('user_id')

    # if not logged int set to none
    # else set g.user by getting user id by id
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

# log user out route
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('blog.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

# go to index page
@bp.route('/')
def index():
    return render_template('blog/index.html')
