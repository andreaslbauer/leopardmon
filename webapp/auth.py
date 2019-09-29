import functools
from dbhelper import dbaccess
import logging

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        organization = request.form['organization']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            doc = dbaccess.dbGetUser(username)
            if (doc != None):
                error = 'User {} is already registered.'.format(username)

        if error is None:
            dbaccess.dbPutUser(username, email, organization, generate_password_hash(password))
            logging.info("Added user %s %s %s", username, email, organization)
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None

        # look up user in database
        doc = dbaccess.dbGetUser(username)
        user = None
        if (doc != None):
            user = doc["name"]

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(doc['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = doc['name']
            return redirect(url_for('home'))

        flash(error)

        logging.info("User logged in %s %s %s", doc["username"], doc["email"], doc["organization"])

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = "andy"


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view



