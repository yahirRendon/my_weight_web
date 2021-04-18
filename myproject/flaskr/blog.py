from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from flask import current_app
from flaskr.auth import login_required
from flaskr.db import get_db
from datetime import datetime

import json

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    """
    go to the index/home page

    :return: index html template
    """ 
    return render_template('blog/index.html')

@bp.route('/user')
def get_user_posts():
    """
    go to the user page

    :return: user html template
    """ 
    return render_template('blog/user.html')

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """
    add a new weight/post entry into the database

    :param GET:     get request
    :param POST:    post request
    :return:        user html template on success
    """ 
    if request.method == 'POST':
        body = request.form['body']
        weight = request.form['weight']
        user_id = session.get('user_id')
        error = None

        if not weight:
            error = 'Weight is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (weight, body, author_id)'
                ' VALUES (?, ?, ?)',
                (weight, body, g.user['id'])
            )
            db.commit()

            return render_template('blog/user.html')

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    """
    get the individual post id for updating

    :param id:           the id of the post
    :param check_author: check user is logged in
    :return: return the post in SQLite3.Row format
    """ 
    post = get_db().execute(
        'SELECT p.id, weight, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """
    update a weight/post entry

    :para id:       the post id
    :param GET:     get request
    :param POST:    post request
    :return:        user html template on success
    """ 
    post = get_post(id)
    user_id = session.get('user_id')

    if request.method == 'POST':
        weight = request.form['weight']
        body = request.form['body']
        error = None

        if not weight:
            error = 'Weight is required.'
        elif not weight.isdigit():
            error = 'Weight must be a number'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET weight = ?, body = ?'
                ' WHERE id = ?',
                (weight, body, id)
            )
            db.commit()
            return render_template('blog/user.html')

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    """
    delete weight/ost entry

    :param id:      the post id
    :param post:    post request
    :return: describe what it returns
    """ 
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

@bp.route('/posts')
def get_all_posts():
    """
    get all the posts from the database 

    :return: json data
    """ 

    # return all posts
    db = get_db()
    posts = db.execute(
        'SELECT p.id, weight, body, created, author_id, username, goalWeight'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    data = json.dumps(posts)

    return data

@bp.route('/user/<int:id>/posts')
def get_all_user_posts(id):
    """
    get all of the posts by user

    :param id: user id
    :return: data as json
    """ 

    # return all posts
    db = get_db()
    posts = db.execute(
        'SELECT p.id, weight, body, created, author_id, username, goalweight'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE u.id = ?'
        ' ORDER BY created DESC',
        (id,)
    ).fetchall()

    # data = json.dumps(tuple(post), indent=4, sort_keys=True, default=str)
    data = json.dumps(posts)

    return data

@bp.route('/getuser') 
def getuser():
    """
    get the user id of logged in user

    :return:    user id as json
    """ 
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
    
    data = json.dumps(user_id)
    return data
