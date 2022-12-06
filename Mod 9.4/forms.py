from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField

class BookForm(FlaskForm):
    title = StringField()
    author= StringField()
    description = TextAreaField()
    year = StringField()
    category = StringField()