from flask import render_template
from flask import Blueprint, request, jsonify, session, redirect, url_for
bp = Blueprint('categories', __name__, url_prefix='/categories')


# Admin-only route: Add a category
@bp.route('/', methods=['POST'])
def add_category():
    from models.category_model import Category
    from database.db import db
    # Check if user is logged in
    if 'user' not in session:
        return jsonify({"error": "Unauthorized access"}), 401

    # Check if user is an admin
    if session['user']['role'] != 'admin':
        return jsonify({"error": "Admin access required"}), 403

     # Handle form data
    category_name = request.form.get('category_name')

    if not category_name:
        return jsonify({"error": "Category name is required"}), 400
    
     # Check if the category already exists
    existing_category = Category.query.filter_by(category_name=category_name).first()
    if existing_category:
        return jsonify({"error": f"Category '{category_name}' already exists"}), 409

    # Add the category to the database
    new_category = Category(category_name=category_name)
    db.session.add(new_category)
    db.session.commit()

    return redirect(url_for('categories.manage_categories'))


@bp.route('/', methods=['GET'])
def manage_categories():
    from models.category_model import Category

    # Query all categories from the database
    categories = Category.query.all()
    print("Categories fetched from database:", categories)  # Debugging

    # Render the template with the list of categories
    return render_template('manage_categories.html', categories=categories)



@bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    from models.category_model import Category
    from database.db import db

    # Check if user is logged in
    if 'user' not in session:
        return jsonify({"error": "Unauthorized access"}), 401

    # Check if user is an admin
    if session['user']['role'] != 'admin':
        return jsonify({"error": "Admin access required"}), 403

    # Fetch the category
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    # Get new category details
    data = request.get_json()
    new_category_name = data.get('category_name')

    if not new_category_name:
        return jsonify({"error": "Category name is required"}), 400

    # Update the category name
    category.category_name = new_category_name
    db.session.commit()

    return jsonify({"message": f"Category '{new_category_name}' updated successfully!"}), 200


@bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    from models.category_model import Category
    from database.db import db

    # Check if user is logged in
    if 'user' not in session:
        return jsonify({"error": "Unauthorized access"}), 401

    # Check if user is an admin
    if session['user']['role'] != 'admin':
        return jsonify({"error": "Admin access required"}), 403

    # Fetch the category
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    # Delete the category
    db.session.delete(category)
    db.session.commit()

    return jsonify({"message": "Category deleted successfully"}), 200


