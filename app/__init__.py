from flask import Flask
from config.settings import Config
from .extensions import db, migrate, login_manager, csrf, limiter
from .auth.routes import auth_bp
from .main.routes import main_bp
from .wallet.routes import wallet_bp
from .admin.routes import admin_bp
import logging
from logging.handlers import RotatingFileHandler
import os

def create_app(config_class=None):
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config_class or Config)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)

    # register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(wallet_bp, url_prefix="/wallet")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(main_bp)

    # logging
    if not os.path.exists("logs"):
        os.makedirs("logs")
    handler = RotatingFileHandler("logs/domainhub.log", maxBytes=1024*1024*5, backupCount=5)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("DomainHub startup")

    # session and security
    app.permanent_session_lifetime = app.config.get("PERMANENT_SESSION_LIFETIME")

    return app