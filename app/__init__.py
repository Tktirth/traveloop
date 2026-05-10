from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()


def create_app(config_object='config.Config'):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # Register blueprints
    from .routes import bp as routes_bp
    from .auth import bp as auth_bp
    app.register_blueprint(routes_bp)
    app.register_blueprint(auth_bp)

    return app

# For Flask CLI
app = create_app()
# Register OAuth blueprints if available
try:
    from .auth import github_bp
    if github_bp.name not in app.blueprints:
        app.register_blueprint(github_bp, url_prefix='/login')
except Exception:
    pass
