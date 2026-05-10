from flask import Blueprint, redirect, url_for, session
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.consumer import oauth_authorized
from .models import User
from . import db, login
from flask_login import login_user
import os

bp = Blueprint('auth', __name__)

# GitHub OAuth blueprint
github_bp = make_github_blueprint(client_id=os.getenv('GITHUB_OAUTH_CLIENT_ID',''), client_secret=os.getenv('GITHUB_OAUTH_CLIENT_SECRET',''))

@bp.route('/login/github')
def login_github():
    return redirect(url_for('github.login'))

@oauth_authorized.connect_via(github_bp)
def github_logged_in(blueprint, token):
    if not token:
        return False
    resp = blueprint.session.get('/user')
    if not resp.ok:
        return False
    info = resp.json()
    provider_id = str(info.get('id'))
    user = User.query.filter_by(provider='github', provider_id=provider_id).first()
    if not user:
        user = User(provider='github', provider_id=provider_id, name=info.get('name'), email=info.get('email'))
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return False

# Register the GitHub blueprint onto the app in create_app dynamically

