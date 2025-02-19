from database.db import db  

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(10), default='user', nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
def __repr__(self):
        return f"<User {self.username}>"