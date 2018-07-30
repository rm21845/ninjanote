from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class NoteForm(FlaskForm):
    message = TextAreaField('Create an encrypted note', validators=[DataRequired(), Length(1,5000)])
    submit = SubmitField("Create note")
    password = PasswordField('Password (optional)', [EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm')


class PassForm(FlaskForm):
    verify = PasswordField('Password', validators=[DataRequired()])
    submitpass = SubmitField("submit")


class ReadForm(FlaskForm):
    read = TextAreaField('Decrypted note', validators=[DataRequired(), Length(1,5000)])
