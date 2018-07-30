import functools
from . import forms
from . import crypto
import bcrypt


from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/password', methods=('GET', 'POST'))
def password():
    form = forms.PassForm()
    return render_template('auth/password.html', form=form)


@bp.route('check', methods=('GET', 'POST'))
def check():
    passwd = request.form['verify']
    note_id = session['id']
    hash_val = str(crypto.hashing(note_id))

    db = get_db()
    cur = db.cursor().execute(
        'SELECT * FROM note WHERE id=?', (hash_val,)
    )
    results = cur.fetchone()

    hashedpw = results['passwd']

    if bcrypt.checkpw(passwd.encode(), hashedpw):
        print('password matched')
        session['pass_match'] = True
        return redirect('/' + str(note_id))
    else:
        print('password unmatched')
        return redirect(url_for('auth.password'))


