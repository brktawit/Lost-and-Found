from flask import Blueprint, session, redirect, url_for
from flask import render_template

bp = Blueprint('logout', __name__, url_prefix='/logout')

@bp.route('/')
def logout_user():
    session.clear()  # ✅ This clears the session completely
    return redirect(url_for('home'))  # Redirect to homepage
