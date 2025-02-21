from database.db import db
from geoalchemy2 import Geometry  # Import Geometry for spatial data
from sqlalchemy.orm import relationship


class Item(db.Model):
    __tablename__ = 'lostitems'

    # Primary key: Unique identifier for the item
    item_id = db.Column(db.Integer, primary_key=True)
    
    # Basic item details
    item_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Foreign Keys
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    category_name = db.Column(db.String(100), nullable=False)  # Store category name directly
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    # Location (Geospatial Point: latitude/longitude)
    location = db.Column(Geometry("POINT", srid=4326), nullable=True) 

    # Place where the items were found
    place = db.Column(db.String(100), nullable=True)  

    # Automatically sets the date when an item is reported
    receiving_date = db.Column(db.Date, server_default=db.func.current_date())
    source = db.Column(db.String(100), nullable=False)

    # Relationships
    category = relationship("Category", back_populates="items")
    user = relationship("User", back_populates="items")

    def __repr__(self):
        return f"<Item {self.item_name} - {self.category_name} - {self.place}>"
