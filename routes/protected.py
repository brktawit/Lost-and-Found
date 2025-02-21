from flask import render_template
from flask import Blueprint, jsonify, session

bp = Blueprint('protected', __name__, url_prefix='/protected')

@bp.route('/', methods=['GET'])
def protected_route():
    """Handles access to a protected route.

    Checks if the user is logged in. If not, returns an unauthorized access error.
    If the user is logged in, returns a success message along with the user's details.

    """
    # Check if the user is in the session to verify login status
    if 'user' not in session:
        return jsonify({"error": "Unauthorized access"}), 401

    # Get the current user's information from the session
    current_user = session['user']
    
    # Return a success message with user information
    return jsonify({
        "message": "Access granted to the protected route!",
        "user": current_user
    }), 200
