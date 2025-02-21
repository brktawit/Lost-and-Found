from flask import Blueprint, session, redirect, url_for


bp = Blueprint('logout', __name__, url_prefix='/logout')

@bp.route('/')
def logout_user():
    """Handles user logout.
    
    Clears the session and redirects the user to the homepage.

    """
    session.clear()  # This clears the session completely
    return redirect(url_for('home'))  # Redirect to homepage

