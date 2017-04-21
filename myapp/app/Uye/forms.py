from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from ..models import Uye

class KayitFormu(FlaskForm):
    """
    this applies anything we want to create a form to register
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('Ad', validators=[DataRequired()])
    last_name = StringField('Soyad', validators=[DataRequired()])
    password = PasswordField('Sifre', validators=[DataRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField('Sifreyi Tekrarlayin')
    adres = StringField('Adres', validators=[DataRequired()])
    submit = SubmitField('Kayit')

    def validate_email(self, field):
        if Uye.query.filter_by(email=field.data).first():
            raise ValidationError('Bu Email adresi zaten kayitlidir.')

    def validate_username(self, field):
        if Uye.query.filter_by(email=field.data).first():
            raise ValidationError('Bu kullanici adi zaten kayitlidir.')

class GirisForm(FlaskForm):
    """
    this form is to sign in
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Sifre', validators=[DataRequired()])
    submit = SubmitField('Giris')
