import os

import click
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


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop')
    def initdb(drop):
        if drop:
            click.confirm('Will delete the database,continue?', abort=True)
            db.drop_all()
            click.echo('Drop database.')
        db.create_all()
        click.echo('Init DB')

    @app.cli.command()
    @click.option('--category', default=10, help='spawn category,default 10')
    @click.option('--post', default=60, help='spawn post, default 60')
    @click.option('--comment', default=300, help='spawn comment, default 300')
    def forge(category, post, comment):
        from Yukiblog.fakes import fake_manager, fake_categories, fake_posts, fake_comments
        
        db.drop_all()
        db.create_all()

        click.echo('gen manager...')
        fake_manager()

        click.echo('gen category...')
        fake_comments(category)

        click.echo('gen posts...')
        fake_posts(post)

        click.echo('gen comment...')
        fake_comments(comment)

        click.echo('gen over')
