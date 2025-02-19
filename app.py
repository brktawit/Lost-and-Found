from flask import render_template, Flask, jsonify, session 
from sqlalchemy import text  # Import the `text` function
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from routes import register, login, categories, protected, logout, items


from database.db import db

app = Flask(__name__)

# Configure Flask session
app.config['SECRET_KEY'] = 'my_secret_key'  # Use a secure, random key

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/Trial'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

from models.category_model import Category
from models.user_model import User
from models.item_model import Item

# Initialize the database
#init_db(app)



# Register routes
app.register_blueprint(register.bp)
app.register_blueprint(login.bp)
app.register_blueprint(categories.bp)
app.register_blueprint(protected.bp)
app.register_blueprint(logout.bp)
app.register_blueprint(items.bp)

# Home route
@app.route("/")
def home():
    # Fetch items grouped by category from the database
    items_by_category = {
        "Electronics": [{"item_name": "Laptop", "description": "A silver laptop found in the library"}],
        "Accessories": [{"item_name": "Watch", "description": "Leather strap watch"}]
    }
    return render_template("home.html", items_by_category=items_by_category)

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
