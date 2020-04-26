from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchTermForm(FlaskForm):
    search_term = StringField('Search Term', validators=[DataRequired()], )
    submit = SubmitField('Submit')
