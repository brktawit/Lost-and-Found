
from flask import render_template
from flask import Blueprint, request, jsonify, session
from models.item_model import Item
from models.category_model import Category

bp = Blueprint('items', __name__, url_prefix='/items')

@bp.route('/add_item', methods=['GET', 'POST'])
def add_item():
    from database.db import db

    if request.method == 'POST':  # Handle form submission
        # Check if the user is logged in
        if 'user' not in session:
            return jsonify({"error": "Unauthorized access"}), 401

        # Get form data
        item_name = request.form.get('item_name')
        description = request.form.get('description')
        category_id = request.form.get('category_id')
        location = request.form.get('location')
        user_id = session['user']['user_id']  # Retrieve logged-in user's ID

        # Validate input
        if not item_name or not category_id:
            return jsonify({"error": "Item name and category ID are required"}), 400

        # Check if category exists
        category = Category.query.get(category_id)
        if not category:
            return jsonify({"error": "Invalid category ID"}), 404

        # Add the item to the database
        new_item = Item(
            item_name=item_name,
            description=description,
            category_id=category_id,
            user_id=user_id,
            location=location
        )
        db.session.add(new_item)
        db.session.commit()

        return render_template('add_item.html', categories=Category.query.all(), success="Item added successfully!")

    # Handle GET request - Render the form
    categories = Category.query.all()  # Fetch all categories for the dropdown
    return render_template("add_item.html", categories=categories)



@bp.route('/', methods=['GET'])  #to handle json file (i will remove this in the future. we dont need it)
def get_items():
    from database.db import db
     # Use a join to include category_name in the query
    items = db.session.query(
        Item.item_id,
        Item.item_name,
        Item.description,
        Category.category_name,  # Fetch category_name from the Category table
        Item.user_id,
        Item.location,
        Item.reported_date
    ).join(Category, Item.category_id == Category.category_id).all()

    # Convert the query results into a list of dictionaries
    item_list = [
        {
            "item_id": item.item_id,
            "item_name": item.item_name,
            "description": item.description,
            "category_name": item.category_name,  # Use category_name instead of category_id
            "user_id": item.user_id,
            "location": item.location,
            "reported_date": item.reported_date
        }
        for item in items
    ]
    return jsonify(item_list), 200



@bp.route('/manage', methods=['GET']) #separate route to handle rendering the HTML
def manage_items():
    from database.db import db
    items = Item.query.all()

    # Use a join to fetch category_name along with items
    items = db.session.query(
        Item.item_id,
        Item.item_name,
        Item.description,
        Category.category_name,
        Item.location
    ).join(Category, Item.category_id == Category.category_id).all()

    # Convert the query results into a list of dictionaries
    item_list = [
        {
            "item_id": item.item_id,
            "item_name": item.item_name,
            "description": item.description,
            "category_name": item.category_name,
            "location": item.location
        }
        for item in items
    ]

    # Pass the item list to the template
    return render_template("manage_items.html", items=item_list)



@bp.route('/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    from database.db import db
    
    
    # Check if the user is logged in
    if 'user' not in session:
        return jsonify({"error": "Unauthorized access"}), 401

    # Fetch the item
    item = Item.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    # Ensure only the creator (based on user_id) or admin can update
    if session['user']['user_id'] != item.user_id and session['user']['role'] != 'admin':
        return jsonify({"error": "Permission denied"}), 403

    # Get updated data from the request
    data = request.get_json()
    item.item_name = data.get('item_name', item.item_name)  # Update item_name if provided
    item.description = data.get('description', item.description)  # Update description if provided

    db.session.commit()  # Save changes to the database

    return jsonify({"message": "Item updated successfully"}), 200



@bp.route('/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    from database.db import db
    # Check if the user is logged in
    if 'user' not in session:
        return jsonify({"error": "Unauthorized access"}), 401

    # Fetch the item
    item = Item.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    # Ensure only the creator (based on user_id) or admin can delete
    if session['user']['user_id'] != item.user_id and session['user']['role'] != 'admin':
        return jsonify({"error": "Permission denied"}), 403

    # Perform the delete
    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": "Item deleted successfully"}), 200
