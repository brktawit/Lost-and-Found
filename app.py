from flask import render_template, Flask, jsonify, session 
from sqlalchemy import text  # Import the `text` function
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from routes import register, login, categories, protected, logout, items
from database.db import db


# Initialize the Flask application
app = Flask(__name__)

# Configure Flask session with a secret key for security
app.config['SECRET_KEY'] = 'my_secret_key'  # Use a secure, random key for production


# Database configuration settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/Trial' # Database connection string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Disable modification tracking

# Initialize the SQLAlchemy object with the app context
db.init_app(app)

# Initialize Flask-Migrate for handling database migrations
migrate = Migrate(app, db)


# Register the routes defined in separate modules
app.register_blueprint(register.bp)
app.register_blueprint(login.bp)
app.register_blueprint(categories.bp)
app.register_blueprint(protected.bp)
app.register_blueprint(logout.bp)
app.register_blueprint(items.bp)


# Home route to render the main page
@app.route("/")
def home():
    print("🔹 Checking session in home:", session)  # Debugging session

    # Check if the user is logged in
    if "user" in session:
        items_by_category = {
            "Electronics": [{"item_name": "Laptop", "description": "A silver laptop found in the library"}],
            "Accessories": [{"item_name": "Watch", "description": "Leather strap watch"}]
        }
        return render_template("home.html", items_by_category=items_by_category, logged_in=True)
    
    return render_template("home.html", logged_in=False)

# creating a route for about.html
@app.route('/about')
def about():
    return render_template('about.html')


# Test the database connection
@app.route("/test-db")
def test_db():
    try:
        # Use the `text` function for the raw SQL query
        result = db.session.execute(text("SELECT 1")).scalar()
        if result == 1:
            return "Database connection is successful!"
        else:
            return "Database connection failed!"
    except Exception as e:
        return f"Database connection error: {e}"

if __name__ == "__main__":
    app.run(debug=True)
