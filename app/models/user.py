from app import db
import bcrypt
from sqlalchemy.orm import validates
import re
from sqlalchemy import text

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user', server_default=text("'user'"))  # 'user' or 'admin'

    # Relationships
    recipes = db.relationship('Recipe', backref='user', lazy=True, cascade='all, delete-orphan')
    favorite_recipes = db.relationship('FavoriteRecipe', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def is_admin(self):
        return self.role == 'admin'

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise ValueError('Email is required')
        
        # Basic email validation pattern
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValueError('Invalid email format')
        
        return email

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError('Username is required')
        if User.query.filter(User.username == username, User.id != self.id).first():
            raise ValueError('Username already exists')
        return username

    @validates('image_url')
    def validate_image_url(self, key, image_url):
        if not image_url:
            raise ValueError('Image URL is required')
        return image_url

    @validates('role')
    def validate_role(self, key, role):
        if role not in ['user', 'admin']:
            raise ValueError('Invalid role. Must be either "user" or "admin"')
        return role

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'image_url': self.image_url,
            'role': self.role
        }
