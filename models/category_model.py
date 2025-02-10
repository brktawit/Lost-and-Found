from database.db import db

class Category(db.Model):
    _tablename_ = 'categories'

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(80), unique=True, nullable=False)

    def _repr_(self):
        return f"<Category {self.category_name}>"
