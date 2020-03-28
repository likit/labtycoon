from flask import Flask


def create_app():
    app = Flask(__name__)

    from main import main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/main')

    from auth import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app