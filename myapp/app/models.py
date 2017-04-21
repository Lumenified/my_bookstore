from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class Uye(UserMixin, db.Model):
    """
    this will provide the core users' table
    """

    # Table names are plural

    __tablename__ = 'uyeler'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    kitaplar = db.relationship('Kitap', backref='uye', lazy='dynamic')
    adres = db.Column(db.String(300), index=True)
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevents password from being accessed
        """
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        """
        Set the password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Checks if hashed password matches the actual one
        """

        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Uye: {}>'.format(self.username)

#this is a user loader
@login_manager.user_loader
def load_user(user_id):
    return Uye.query.get(int(user_id))



class Kategori(db.Model):
    """
    This for the categories that the books have
    """
    __tablename__ = 'kategoriler'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    kitaplar = db.relationship('Kitap', backref='kategori',
                                                lazy='dynamic')
    def __repr__(self):
        return '<Kategori: {}>'.format(self.name)

class Kitap(db.Model):
    """
    This creates the book table as we mentioned above, plural and lowercased ;)
    """

    __tablename__ = 'kitaplar'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    uye_id = db.Column(db.Integer, db.ForeignKey('uyeler.id'))
    kategori_id = db.Column(db.Integer, db.ForeignKey('kategoriler.id'))

    def __repr__(self):
        return '<Kitap: {}>'.format(self.name)

"""
to initialize the database, we use flask db init, then flask db migrate, then flask db upgrade -in order-
"""
