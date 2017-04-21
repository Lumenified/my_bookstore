from flask import flash, redirect, render_template, url_for, abort
from flask_login import login_user, login_required, logout_user

from . import uye
from forms import GirisForm, KayitFormu
from .. import db
from ..models import Uye

@uye.route('/kayit', methods=['GET', 'POST'])
def kayit():
    """
    this handles the registration
    """
    form = KayitFormu()
    if form.validate_on_submit():
        uye = Uye(email=form.email.data,
                    username=form.username.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    password=form.password.data,
                    adres=form.adres.data)
        db.session.add(uye)
        db.session.commit()
        flash('Basariyla kaydedildi.')

        return redirect(url_for('uye.giris'))

    return render_template('uye/kayit.html',form=form, title='Kayit')

@uye.route('/giris', methods=['GET', 'POST'])
def giris():
    """
    this handles signing in
    """
    form = GirisForm()
    if form.validate_on_submit():
        uye = Uye.query.filter_by(email=form.email.data).first()
        if uye is not None and uye.verify_password(form.password.data):
            login_user(uye)
            return redirect(url_for('home.dashboard'))
        else:
            flash('Kullanici adiniz veya sifreniz hatali.')

    return render_template('uye/giris.html', form=form, title='Giris')

@uye.route('/cikis')
@login_required
def cikis():
    """
    this is for logging out securily,
    """
    logout_user()
    flash('Basariyla cikis yaptiniz')

    return redirect(url_for('uye.giris'))
