from app import db
from sqlalchemy.orm import validates
from flask import current_app

class FavoriteRecipe(db.Model):
    __tablename__ = 'favorite_recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    procedure = db.Column(db.Text, nullable=False)
    people_served = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    cooking_time = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    video_link = db.Column(db.String(255), nullable=False)
    
    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @validates('category')
    def validate_category(self, key, category):
        if category not in current_app.config['VALID_CATEGORIES']:
            raise ValueError(f"Category must be one of: {', '.join(current_app.config['VALID_CATEGORIES'])}")
        return category

    @validates('rating')
    def validate_rating(self, key, rating):
        if not isinstance(rating, (int, float)) or rating < 0 or rating > 5:
            raise ValueError("Rating must be a number between 0 and 5")
        return rating

    @validates('people_served')
    def validate_people_served(self, key, people_served):
        if not isinstance(people_served, int) or people_served <= 0:
            raise ValueError("People served must be a positive integer")
        return people_served

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'country': self.country,
            'rating': self.rating,
            'ingredients': self.ingredients,
            'procedure': self.procedure,
            'people_served': self.people_served,
            'category': self.category,
            'cooking_time': self.cooking_time,
            'image_url': self.image_url,
            'video_link': self.video_link,
            'user_id': self.user_id,
            'user': self.user.username
        }
