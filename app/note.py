import functools
from app.db import get_db
from . import crypto
from . import forms


from flask import (
    Blueprint, g, redirect, render_template, request, url_for, session
)

bp = Blueprint('note', __name__)


@bp.route('/')
def note():
    form = forms.NoteForm()
    return render_template('note/index.html', form=form)


@bp.route('/<note_id>')
def read(note_id=None, passwd_match=False):
    form = forms.ReadForm()
    form.read.data = 'Error'
    hash_val = str(crypto.hashing(note_id))

    db = get_db()
    cur = db.cursor().execute(
        'SELECT * FROM note WHERE id=?', (hash_val,)
    )
    results = cur.fetchone()

    db_hash = results['id']
    crypted_content = results['content']
    passwd = results['passwd']

    if passwd and session['pass_match'] is False:
        session['id'] = note_id
        return redirect(url_for('auth.password'))

    if hash_val == db_hash:
        print('[+]id and hash_id matched!')
        if type(crypted_content) == str:
            message = 'Note has been destroyed'
        else:
            message = crypto.aes_decrypt(note_id, crypted_content).decode('utf-8')
            #  message = (message).decode('utf-8')
            crypto.destroy_note(hash_val)

        form.read.data = message

    return render_template('note/read.html', form=form)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    form = forms.NoteForm()
    session['pass_match'] = False

    if request.form['message'] and request.method == 'POST':
        note_id = crypto.id_generator()
        hash_val = str(crypto.hashing(note_id))
        contents = crypto.aes_encrypt(note_id, request.form['message'])

        if request.form['password']:
            hashedpwd = crypto.pass_encrypt(request.form['password'])
        else:
            hashedpwd = None

        db = get_db()
        db.execute(
            "INSERT INTO note VALUES (?, ?, ?)", (hash_val, contents, hashedpwd)
        )
        db.commit()
        note_id = 'http://localhost:5000/' + str(note_id)
        return render_template('note/index.html', note_id=note_id, form=form)

