from flask import Blueprint, jsonify, session
from flask import render_template

bp = Blueprint('logout', __name__, url_prefix='/logout')

@bp.route('/', methods=['POST'])
def logout_user():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200
