from flask import Blueprint, request, jsonify, session, redirect, url_for
from database.db import db
from flask import render_template
from models.category_model import Category


bp = Blueprint('categories', __name__, url_prefix='/categories')

"""
Routes for managing categories in the Lost and Found system.
Only admins can add, update, and delete categories.
"""


# Admin-only route: Add a category
@bp.route('/', methods=['POST'])
def add_category():
    """
    Adds a new category.
    Only accessible by admins.

    Responses:
    - 201: Category added successfully
    - 400: Missing category name
    - 401: Unauthorized access
    - 403: Admin access required
    - 409: Category already exists
    """
    
    
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
    """
    Retrieves all categories.

    """
    
    categories = Category.query.all()
    
    # Render the template with the list of categories
    return render_template('manage_categories.html', categories=categories)



@bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    """
    Updates an existing category.
    Only accessible by admins.

    """

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
    """
    Deletes a category.
    Only accessible by admins.

    """
   
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


