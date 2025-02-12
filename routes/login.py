from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash
from flask import render_template

bp = Blueprint('login', __name__, url_prefix='/login')

@bp.route('/', methods=['GET', 'POST'])
def login_user():
    from models.user_model import User

    if request.method == 'POST':  # Handle form submission
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        user = User.query.filter_by(username=username).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({"error": "Invalid credentials"}), 401

        # ✅ Set user details in the session
        session['user'] = {
            'user_id': user.user_id,
            'username': user.username,
            'role': user.role
        }

        print("🔹 Session after login:", session)  # Debugging session data

        return jsonify({"message": "Login successful"}), 200

    return render_template("login.html")