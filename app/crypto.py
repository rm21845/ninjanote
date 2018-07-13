import random
import hashlib
import base64
import sys
from cryptography.fernet import Fernet
from app.db import get_db


def aes_decrypt(key, crypted_content):
    encoded_key = str(key).encode()
    p = base64.urlsafe_b64encode(encoded_key)
    f = Fernet(p)
    return f.decrypt(crypted_content)


def aes_encrypt(key, message):
    encoded_key = str(key).encode()
    p = base64.urlsafe_b64encode(encoded_key)
    f = Fernet(p)
    return f.encrypt(message.encode())


def hashing(note_id):
    """
    :param id: id of note
    :return: hashed value of note id
    """
    hash_val = hashlib.sha3_256()
    hash_val.update((str(note_id).encode()))
    return hash_val.hexdigest()


def destroy_note(hash_id):
    """
        Destroys the encrypted note
    :param hash_id: ID of note found in url
    """
    db = get_db()
    db.execute(
        "UPDATE note SET content = 'Note has been destroyed' WHERE id=?", (hash_id,)
    )
    db.commit()


def id_generator():
    random.seed()
    return random.getrandbits(106)
