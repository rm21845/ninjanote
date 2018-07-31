from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class NoteForm(FlaskForm):
    message = TextAreaField('Create an encrypted note', validators=[DataRequired(), Length(1, 5000)])
    submit = SubmitField("Create note")
    password = PasswordField('Password (optional)', [EqualTo('confirm', message='Passwords must match'), Length(6, 64)])
    confirm = PasswordField('Confirm')


class PassForm(FlaskForm):
    verify = PasswordField('Enter password for note', validators=[DataRequired(), Length(6, 64)])
    submitpass = SubmitField("submit")


class ReadForm(FlaskForm):
    read = TextAreaField('Decrypted note', validators=[DataRequired(), Length(1,5000)])
