from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash
from flask import render_template
from models.user_model import User

bp = Blueprint('login', __name__, url_prefix='/login')

@bp.route('/', methods=['GET', 'POST'])
def login_user():
    """Handles user login.

    If the request method is POST, it checks the provided username and password,
    validates them against the database, and stores user details in the session.
    If the request method is GET, it renders the login page.
    
    Returns:
        Response: JSON response with login status or renders login template.
    """

    if request.method == 'POST':  # Handle form submission
        # Retrieve the JSON data sent with the request
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Validate input: Ensure username and password are provided
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        # Query the database for the user by username
        user = User.query.filter_by(username=username).first()
        
         # Check if the user exists and validate the password
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({"error": "Invalid credentials"}), 401

         # Store user details in the session upon successful login
        session['user'] = {
            'user_id': user.user_id,
            'username': user.username,
            'role': user.role
        }


        # Return a successful login response with user details
        return jsonify({
            "message": "Login successful",
            "user_id": user.user_id,
            "role": user.role,
            "redirect": "/"  #Redirect after successful login
        }), 200

    return render_template("login.html")
