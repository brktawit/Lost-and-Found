from flask import render_template, Blueprint, request, jsonify, session
from sqlalchemy import func
from geoalchemy2.functions import ST_X, ST_Y
from models.item_model import Item
from models.category_model import Category
from models.user_model import User
from database.db import db

bp = Blueprint('items', __name__, url_prefix='/items')

# Helper function to convert Well-Known Text (WKT) to a dictionary of latitude and longitude
def wkt_to_dict(wkt):
    if wkt:
        coords = wkt.replace("POINT(", "").replace(")", "").split()
        return {"longitude": float(coords[0]), "latitude": float(coords[1])}
    return None

# ------------------- ADD ITEM ------------------- #
@bp.route('/add_item', methods=['GET', 'POST'])
def add_item():
    """Handles adding a new item to the database."""

    if request.method == 'POST':  # Handle form submission
        
        # Check if the user is logged in
        if 'user' not in session:
            return jsonify({"error": "Unauthorized access"}), 401

        # Get form data
        item_name = request.form.get('item_name')
        description = request.form.get('description')
        category_id = request.form.get('category_id')
        place = request.form.get('place')  # station_name stored in place
        user_id = session['user']['user_id']  # Retrieve logged-in user's ID
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')

        # Validate required input
        if not item_name or not category_id or not latitude or not longitude:
            return jsonify({"error": "Item name, category, and location are required"}), 400
        
        # Convert latitude and longitude to PostGIS POINT format
        location = func.ST_Point(float(longitude), float(latitude), 4326)
        
        # Check if user exists in the database before proceeding
        user = db.session.query(User).filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        

        # Determine the source of the item (username or "unknown")
        source = user.username if user else "unknown"

        # Check if category exists
        category = Category.query.get(category_id)
        if not category:
            return jsonify({"error": "Invalid category ID"}), 404


        # Create a new item instance and add it to the database
        new_item = Item(
            item_name=item_name,
            description=description,
            category_id=category_id,
            category_name=category.category_name,  # Store category name directly
            user_id=user_id,
            location=location,
            place=place,
            source=source
        )
        db.session.add(new_item)
        db.session.commit()

        return render_template('add_item.html', categories=Category.query.all(), success="Item added successfully!")

    # Handle GET request - Render the item addition form
    categories = Category.query.all()  # Fetch all categories for the dropdown
    return render_template("add_item.html", categories=categories)



# ------------------- GET ALL ITEMS ------------------- #
@bp.route('/', methods=['GET'])
def get_items():
    """Retrieves a paginated list of items, optionally filtered by category or search query."""

    # Get the logged-in user's ID and role
    current_user = session.get("user", {})
    user_id = current_user.get("user_id")
    user_role = current_user.get("role")


    # Get query parameters for pagination and filtering
    page = request.args.get('page', 1, type=int)  # Default to page 1
    limit = request.args.get('limit', 10, type=int)  # Default limit is 10 items per page
    category_filter = request.args.get('category', None)  # Get category filter from API request
    search_query = request.args.get('search', "").strip().lower()  # Get search term

# Define the base query for items`
    items_query = db.session.query(
        Item.item_id,
        Item.item_name,
        Item.description,
        Item.category_id,
        Item.category_name,  # Fetch category_name for clarity
        Item.user_id,
        User.username.label("username"),   # Fetch username associated with the item
        ST_X(Item.location).label("longitude"),  # Extract longitude
        ST_Y(Item.location).label("latitude"),   # Extract latitude
        Item.place,
        Item.source,
        Item.receiving_date

    ).outerjoin(User, Item.user_id == User.user_id)  # Join with User to get usernames


     # If the user is NOT an admin, filter to show only their own items
    if user_role != "admin":
        items_query = items_query.filter(Item.user_id == user_id)

     # Apply search filter if a search query is provided
    if search_query:
        items_query = items_query.filter(
        db.or_(
            Item.item_name.ilike(f"%{search_query}%"),  # Search by item name
            Item.source.ilike(f"%{search_query}%"),  # Search by source
            Item.place.ilike(f"%{search_query}%")  # Search by place
        )
    )

     # Apply category filter if provided
    if category_filter:
        items_query = items_query.filter(Item.category_name == category_filter)

     # Pagination Logic 
    total_items = items_query.count()  # Total number of items
    items = items_query.offset((page - 1) * limit).limit(limit).all()  # Apply pagination


    # Convert query results into a list of dictionaries(JSON format)
    item_list = [
        {
            "item_id": item.item_id,
            "item_name": item.item_name,
            "description": item.description,
            "category_id": item.category_id,
            "category_name": item.category_name,
            "user_id": item.user_id,
            "username": item.username if item.username else "Unknown",
            "latitude": item.latitude,
            "longitude": item.longitude,
            "place": item.place,
            "source": item.source,
            "receiving_date": item.receiving_date,
            
        }

        for item in items
    ]
     # Return paginated data with total items and page information
    return jsonify({
        "total_items": total_items,
        "page": page,
        "limit": limit,
        "total_pages": (total_items // limit) + (1 if total_items % limit > 0 else 0),
        "items": item_list
    }), 200
  


# ------------------- MANAGE ITEMS (HTML RENDER) ------------------- #
@bp.route('/manage', methods=['GET'])
def manage_items():
    """Renders the management interface for items."""

    categories = Category.query.all()  # Fetch categories from the database
    return render_template("manage_items.html", categories=categories)



# ------------------- UPDATE ITEM ------------------- #
@bp.route('/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """Updates an existing item's details."""

    # Check if the user is logged in
    if 'user' not in session:
        return jsonify({"error": "Unauthorized access"}), 401
    
    user_role = session['user']['role']
    user_id = session['user']['user_id']

    # Fetch the item to update
    item = Item.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    # Admins can edit all items
    if user_role != 'admin' and item.source == "admin":
        return jsonify({"error": "You are not allowed to edit this item."}), 403

    # Regular users can only edit their own items
    if user_role != "admin" and item.user_id != user_id:
        return jsonify({"error": "Permission denied"}), 403

    # Get updated data from the request
    data = request.get_json()
    item.item_name = data.get('item_name', item.item_name) # Update item name if provided
    item.description = data.get('description', item.description) # Update description if provided
    item.place = data.get('place', item.place)   # Update place if provided

     # Update location if both latitude and longitude are provided
    if "latitude" in data and "longitude" in data:
        item.location = func.ST_Point(float(data["longitude"]), float(data["latitude"]), 4326)

     # Commit changes to the database
    db.session.commit()
    return jsonify({"message": "Item updated successfully"}), 200



# ------------------- DELETE ITEM ------------------- #
@bp.route('/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Deletes an existing item from the database."""

    # Check if the user is logged in
    if 'user' not in session:
        return jsonify({"error": "Unauthorized access"}), 401
    
    user_role = session['user']['role']
    user_id = session['user']['user_id']

    # Fetch the items to delete
    item = Item.query.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    # Admins can delete all items
    if user_role != 'admin' and item.source == "admin":
        return jsonify({"error": "You are not allowed to delete this item."}), 403

    #  Regular users can only delete their own items
    if user_role != "admin" and item.user_id != user_id:
        return jsonify({"error": "Permission denied"}), 403

    # Delete the item and commit changes to the database
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted successfully"}), 200


