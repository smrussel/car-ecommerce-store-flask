import logging
from flask import Flask
from config import Config
from flask_uploads import IMAGES, UploadSet, configure_uploads
from flask_mail import Mail
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask_moment import Moment
from flask_gravatar import Gravatar
from flask_ckeditor import CKEditor


basedir = os.path.abspath(os.path.dirname(__file__))

mail = Mail()
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager() 
bootstrap = Bootstrap()
moment = Moment()
ckeditor = CKEditor()

photos = UploadSet('photos', IMAGES)

login.login_view = 'auth.login'
login.login_message_category = "info"

# define the name of your app below
APP_NAME = 'Car Zone'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/uploaded-images')
    configure_uploads(app, photos)
    db.init_app(app)
    login.init_app(app)
    bootstrap.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False,
                        use_ssl=False, base_url=None)

    # import the blueprint
    from app.auth.routes import auth
    from app.main.routes import main
    from app.cars.routes import cars
    from app.errors.handlers import errors
    from app.admin.routes import admin_bp
    from app.pages.routes import pages
    from app.blog.routes import blogs
    from app.cart.routes import cart_bp
    from app.checkout.routes import checkout
    from app.rss.routes import rss_bp
    # register the blueprint
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(main, url_prefix="/")
    app.register_blueprint(cars, url_prefix="/")
    app.register_blueprint(errors, url_prefix="/")
    app.register_blueprint(admin_bp, url_prefix="/")
    app.register_blueprint(pages, url_prefix="/")
    app.register_blueprint(blogs, url_prefix="/")
    app.register_blueprint(cart_bp, url_prefix="/")
    app.register_blueprint(checkout, url_prefix="/")
    app.register_blueprint(rss_bp, url_prefix="/")

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject=f'{APP_NAME} Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(f'logs/{APP_NAME.lower()}.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info(f'{APP_NAME} startup')

    @app.before_first_request
    def create_tables():
        db.create_all()

    return app