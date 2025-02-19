from database.db import db

class Item(db.Model):
    __tablename__ = 'lostitems'

    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    location = db.Column(db.String(100), nullable=True)
    reported_date = db.Column(db.Date, server_default=db.func.current_date())

    def __repr__(self):
        return f"<Item {self.item_name}>"
