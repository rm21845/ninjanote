from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class NoteForm(FlaskForm):
    message = TextAreaField('notepad', validators=[DataRequired(), Length(1,5000)])
    submit = SubmitField("create")
