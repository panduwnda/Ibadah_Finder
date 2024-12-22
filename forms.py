# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class TempatIbadahForm(FlaskForm):
    nama = StringField('Nama Tempat Ibadah', validators=[DataRequired()])
    luas = DecimalField('Luas', validators=[DataRequired()])
    remark = TextAreaField('Remark')
    latitude = DecimalField('Latitude', validators=[DataRequired()])
    longitude = DecimalField('Longitude', validators=[DataRequired()])
    submit = SubmitField('Tambah Tempat Ibadah')
