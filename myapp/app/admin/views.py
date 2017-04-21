from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import KategoriForm, KitapForm, UyeForm
from .. import db
from ..models import Kategori, Kitap, Uye

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

# Category Views

@admin.route('/kategori', methods=['GET', 'POST'])
@login_required
def kategori_liste():
    """
    Lists all categories
    """
    check_admin()

    kategoriler = Kategori.query.all()

    return render_template('admin/kategoriler/kategoriler.html',
                           kategoriler=kategoriler, title="Kategori")

@admin.route('/kategori/ekle', methods=['GET', 'POST'])
@login_required
def kategori_ekle():
    """
    Add a category to the database
    """
    check_admin()

    kategori_ekle = True

    form = KategoriForm()
    if form.validate_on_submit():
        kategori = Kategori(name=form.name.data)
        try:
            # add category to the database
            db.session.add(kategori)
            db.session.commit()
            flash('Basariyla bir kategori olusturdunuz.')
        except:
            # in case category name already exists
            flash('Error: Bu kategori zaten kayitlidir.')

        # redirect to categories page
        return redirect(url_for('admin.kategori_liste'))

    # load category template
    return render_template('admin/kategoriler/kategori.html', action="Add",
                           kategori_ekle=kategori_ekle, form=form,
                           title="Kategori Ekle")
@admin.route('/kategoriler/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def kategori_duzenle(id):
    """
    Edit a category
    """
    check_admin()

    kategori_ekle = False

    kategori = Kategori.query.get_or_404(id)
    form = KategoriForm(obj=kategori)
    if form.validate_on_submit():
        kategori.name = form.name.data
        db.session.commit()
        flash('Basariyla kategoriyi degistirdiniz')

        # redirect to the categories page
        return redirect(url_for('admin.kategori_liste'))

    form.name.data = kategori.name
    return render_template('admin/kategoriler/kategori.html', action="Edit",
                           kategori_ekle=kategori_ekle, form=form,
                           kategori=kategori, title="Kategori Duzenle")

#######################################################################
########### Kitap view ##############
######################

@admin.route('/kitaplar')
@login_required
def kitap_liste():
    check_admin()
    """
    list all books
    """
    kitaplar = Kitap.query.all()
    return render_template('admin/kitaplar/kitaplar.html', kitaplar=kitaplar,
                            title='Kitaplar')

@admin.route('kitaplar/ekle', methods=['GET', 'POST'])
@login_required
def kitap_ekle():
    """
    Adds Books
    """
    check_admin()

    kitap_ekle = True

    form = KitapForm()
    if form.validate_on_submit():
        kitap = Kitap(name=form.name.data, description=form.description.data,
                        kategori=form.kategori.data)
        try:
            db.session.add(kitap)
            db.session.commit()
        except:
            flash('Bu kitap zaten kayitlidir.')

        return redirect(url_for('admin.kitap_liste'))

    return render_template('admin/kitaplar/kitap.html', kitap_ekle=kitap_ekle,
                            form=form, title='Kitap Ekle')

@admin.route('/kitaplar/duzenle/<int:id>', methods=['GET', 'POST'])
@login_required
def kitap_duzenle(id):
    """
    Edits a book
    """
    check_admin()

    kitap_ekle = False

    kitap = Kitap.query.get_or_404(id)
    form = KitapForm(obj=kitap)
    if form.validate_on_submit():
        kitap.name = form.name.data
        kitap.description = form.description.data
        kitap.kategori = form.kategori.data
        db.session.add(kitap)
        db.session.commit()
        flash('Basariyla degistirdiniz.')

        # redirect to the books page
        return redirect(url_for('admin.kitap_liste'))

    form.description.data = kitap.description
    form.name.data = kitap.name
    form.kategori.data = kitap.kategori
    return render_template('admin/kitaplar/kitap.html', kitap_ekle=kitap_ekle,
                           form=form, title="Kitap Duzenle")

@admin.route('/kitaplar/sil/<int:id>', methods=['GET', 'POST'])
@login_required
def kitap_sil(id):
    """
    Deletes a book from the database
    """
    check_admin()

    kitap = Kitap.query.get_or_404(id)
    db.session.delete(kitap)
    db.session.commit()
    flash('Basariyla sildiniz.')

    # redirect to the books page
    return redirect(url_for('admin.kitap_liste'))

    return render_template(title="Kitap Sil")


###################################################
################ Kiralama ####################
###############################

@admin.route('/kiralama')
@login_required
def kiralama_listesi():
    """
    Lists all books can be rented
    """

    check_admin()

    uyeler = Uye.query.all()

    return render_template('admin/kiralama/listesi.html', uyeler=uyeler,
                            title='Kitap Listesi')

@admin.route('/kiralama/kirala/<int:id>', methods=['GET', 'POST'])
@login_required
def kitap_kirala(id):
    """
    Shows the list of the books can be rented for the users, not admins.
    It will pop N/A for the lovely admins
    """
    check_admin()

    uye = Uye.query.get_or_404(id)

    # prevent admin from being renting a book
    if uye.is_admin:
        abort(403)

    form = UyeForm(obj=uye)
    if form.validate_on_submit():
        yeni_kitap = form.kitap.data
        yeni_kitap.uye = Uye.query.filter_by(id=id).first()
        db.session.add(yeni_kitap)
        db.session.commit()
        flash('Kiralama islemi gerceklesmistir.')
        # redirect to the renting page
        return redirect(url_for('admin.kiralama_listesi'))

    return render_template('admin/kiralama/kirala.html',
                           uye=uye, form=form,
                           title='Kitap Kirala')
