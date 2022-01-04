from flask import Flask
from flask_mail import Mail
from config import Config
from libs.database import init_db
from libs.middleware import init_middlewares
from libs.depends.register import register_all

def create_app():
    """App factory function"""

    app = Flask(__name__)
    app.config_class = Config

    Mail(app)
    init_db(app)
    init_middlewares(app)

    from apps.api_v1 import api_blueprint as api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')

    return app

register_all()
app = create_app()
