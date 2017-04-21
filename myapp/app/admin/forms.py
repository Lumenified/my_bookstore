# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Kitap, Kategori

class KategoriForm(FlaskForm):
    """
    Form for admin to add or edit a categories
    """
    name = StringField('isim', validators=[DataRequired()])
    submit = SubmitField('Kaydet')


class KitapForm(FlaskForm):
    """
    Form for admin to add or edit a book
    """
    name = StringField('Isim', validators=[DataRequired()])
    description = StringField('Tanim', validators=[DataRequired()])
    kategori = QuerySelectField(query_factory=lambda: Kategori.query.all(),
                                get_label="name")
    submit = SubmitField('Kaydet')

class UyeForm(FlaskForm):
    """
    Form for Subs to rent a book
    """
    kitap = QuerySelectField(query_factory=lambda: Kitap.query.filter_by(uye_id=None).all(),
                            get_label="name")
    submit = SubmitField('Kaydet')
