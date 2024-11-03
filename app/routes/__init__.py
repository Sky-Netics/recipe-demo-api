from .auth import auth_bp
from .users import users_bp
from .recipes import recipes_bp
from .favorite_recipes import favorite_recipes_bp

__all__ = ['auth_bp', 'users_bp', 'recipes_bp', 'favorite_recipes_bp']
