import os
from flask import Flask

from Yukiblog.blueprints.auth import auth_bp
from Yukiblog.blueprints.blog import blog_bp
from Yukiblog.blueprints.manager import manager_bp
from Yukiblog.plugins import bootstrap, db, moment, ckeditor, mail
from Yukiblog.configs import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('Yukiblog')
    app.config.from_object(config[config_name])

    # 插件初始化
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)

    app.register_blueprint(blog)
    app.register_blueprint(manager, url_prefix='/manager')
    app.register_blueprint(auth, url_prefix='/auth')
    return app


def register_logging(app):
    pass  # 暂留


def register_blueprints(app):
    app.register_blueprint(blog)
    app.register_blueprint(manager, url_prefix='/manager')
    app.register_blueprint(auth, url_prefix='/auth')


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_template_context(app):
    pass
