from database.db import db  
from sqlalchemy.orm import relationship


class User(db.Model):
    """
    Represents a system user.
    
    items (relationship): Relationship to the `Item` model, representing items reported by the user.
    """
    
    
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False) # Ensure this is securely hashed
    role = db.Column(db.String(10), default='user', nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationship: One user can report multiple items
    items = relationship("Item", back_populates="user", lazy="dynamic") # Lazy loading for better performance
   
    def __repr__(self):
        return f"<User {self.username}>"
