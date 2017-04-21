from flask import abort, Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

from config import app_config



db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name):
    """
    Main app settings
    """

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)

    """
    LoginManager settings
    """
    login_manager.init_app(app)
    login_manager.login_message = "Lutfen uye olunuz."
    login_manager.login_view = "uye.giris"

    migrate = Migrate(app, db)
    Bootstrap(app)

    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .Uye import uye as uye_blueprint
    app.register_blueprint(uye_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/Yasak.html', title='Yasak'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Sayfa Bulunamadi'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Server Hatasi'), 500


    return app
