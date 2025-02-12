from flask import render_template
from flask import Blueprint, jsonify, session

bp = Blueprint('protected', __name__, url_prefix='/protected')

@bp.route('/', methods=['GET'])
def protected_route():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized access"}), 401

    current_user = session['user']
    return jsonify({
        "message": "Access granted to the protected route!",
        "user": current_user
    }), 200
