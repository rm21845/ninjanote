import functools
from app.db import get_db
from . import crypto
from . import forms


from flask import (
    Blueprint, g, redirect, render_template, request, url_for
)

bp = Blueprint('note', __name__)


@bp.route('/')
@bp.route('/<note_id>')
def note(note_id=None):
    form = forms.NoteForm()
    if note_id:
        message = 'Note not found'
        hash_val = str(crypto.hashing(note_id))

        db = get_db()
        cur = db.cursor().execute(
            'SELECT * FROM note WHERE id=?', (hash_val,)
        )
        result =[x for x in cur.fetchone()]
        db_hash, crypted_content = result[0], result[1]
        print('db hash:' + db_hash)

        if hash_val == db_hash:
            print('[+]id and hash_id matched!')
            destroyed = 'Note has been destroyed'
            if type(crypted_content) == str:
                message = destroyed
            else:
                message = crypto.aes_decrypt(note_id, crypted_content)
                message = (message).decode('utf-8')
                crypto.destroy_note(hash_val)

            form.message.data = message

        return render_template('note/index.html', form=form)
    else:
        return render_template('note/index.html', form=form)


@bp.route('/create', methods=('GET','POST'))
def create():
    form = forms.NoteForm()
    if request.form['message'] and request.method == 'POST':
        note_id = crypto.id_generator()
        hash_val = str(crypto.hashing(note_id))
        contents = crypto.aes_encrypt(note_id, request.form['message'])

        db = get_db()
        db.execute(
            "INSERT INTO note VALUES (?, ?)", (hash_val, contents)
        )
        db.commit()

        return render_template('note/index.html', note_id = note_id, form=form)

