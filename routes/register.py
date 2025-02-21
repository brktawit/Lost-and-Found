from flask import render_template
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from database.db import db
from models.user_model import User



bp = Blueprint('register', __name__, url_prefix='/register')

@bp.route('/', methods=['GET', 'POST'])
def register_user():
    """Handles user registration.
    Accepts user details via POST request and registers a new user if the username
    is unique. If the registration is successful, returns a success message.
    """

    if request.method == 'POST':  # Handle form submission
        data = request.get_json() # Get JSON data from request

        # Extract username and password from the request data
        username = data.get('username')
        password = data.get('password')

        # Validate input
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # Check if username already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"error": "Username already exists"}), 409

        # Hash the password for security
        hashed_password = generate_password_hash (password)
        
        # Create a new user instance and add it to the database
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    # Render the registration form for GET requests
    return render_template("register.html")
