from database.db import db
from sqlalchemy.orm import relationship


class Category(db.Model):
     """
    This Represents a category of lost items.

    Attributes:
        category_id (int): The unique identifier for the category.
        category_name (str): The name of the category (must be unique).
        items (relationship): Establishes a one-to-many relationship with the Item model.
    """
     __tablename__ = 'categories'
     category_id = db.Column(db.Integer, primary_key=True)
     category_name = db.Column(db.String(80), unique=True, nullable=False)
     
    # Relationship with Item model (One category can have multiple items)
     items = relationship("Item", back_populates="category")
     
     def __repr__(self):
        """Returns a string representation of the category."""
        return f"<Category {self.category_name}>"
