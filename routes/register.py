from flask import render_template
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash



bp = Blueprint('register', __name__, url_prefix='/register')

@bp.route('/', methods=['GET', 'POST'])
def register_user():
    from database.db import db
    from models.user_model import User

    if request.method == 'POST':  # Handle form submission
        data = request.get_json()

        # Extract username and password
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"error": "Username already exists"}), 409

        # Hash the password and create a new user 
        hashed_password = generate_password_hash (password)
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    # Render the registration form for GET requests
    return render_template("register.html")
