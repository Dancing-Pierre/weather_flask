from flask_wtf import FlaskForm
from wtforms import StringField


class SearchForm(FlaskForm):
    city = StringField('城市')
    date = StringField('日期')
