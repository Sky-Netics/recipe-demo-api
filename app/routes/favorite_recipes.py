from flask import Blueprint
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import FavoriteRecipe
from app import db
from app.api_models import api, recipe_input, recipe_output, error_model

favorite_recipes_ns = Namespace('favorite_recipes', description='Favorite recipe operations')
api.add_namespace(favorite_recipes_ns)

@favorite_recipes_ns.route('/favorite_recipes')
class FavoriteRecipeList(Resource):
    @jwt_required()
    @favorite_recipes_ns.doc(security='Bearer Auth')
    @favorite_recipes_ns.response(200, 'Success', [recipe_output])
    def get(self):
        """Get all favorite recipes for the current user"""
        current_user_id = get_jwt_identity()
        favorite_recipes = FavoriteRecipe.query.filter_by(user_id=current_user_id).all()
        return [recipe.to_dict() for recipe in favorite_recipes], 200

    @jwt_required()
    @favorite_recipes_ns.doc(security='Bearer Auth')
    @favorite_recipes_ns.expect(recipe_input)
    @favorite_recipes_ns.response(201, 'Recipe added to favorites successfully', recipe_output)
    @favorite_recipes_ns.response(422, 'Validation error', error_model)
    def post(self):
        """Add a recipe to favorites"""
        current_user_id = get_jwt_identity()
        data = favorite_recipes_ns.payload

        try:
            # Add current user_id to favorite recipe data
            data['user_id'] = current_user_id
            
            # Create new favorite recipe
            favorite_recipe = FavoriteRecipe(**data)
            db.session.add(favorite_recipe)
            db.session.commit()

            return favorite_recipe.to_dict(), 201

        except ValueError as e:
            return {"errors": [str(e)]}, 422
        except Exception as e:
            db.session.rollback()
            return {"errors": ["An error occurred while adding the recipe to favorites"]}, 500

@favorite_recipes_ns.route('/favorite_recipes/<int:id>')
class FavoriteRecipeDetail(Resource):
    @jwt_required()
    @favorite_recipes_ns.doc(security='Bearer Auth')
    @favorite_recipes_ns.expect(recipe_input)
    @favorite_recipes_ns.response(200, 'Favorite recipe updated successfully', recipe_output)
    @favorite_recipes_ns.response(401, 'Not authorized', error_model)
    @favorite_recipes_ns.response(404, 'Favorite recipe not found', error_model)
    @favorite_recipes_ns.response(422, 'Validation error', error_model)
    def patch(self, id):
        """Update a favorite recipe"""
        current_user_id = get_jwt_identity()
        favorite_recipe = FavoriteRecipe.query.get_or_404(id)

        # Check if the current user owns the favorite recipe
        if favorite_recipe.user_id != current_user_id:
            return {"errors": ["Not authorized to update this favorite recipe"]}, 401

        try:
            data = favorite_recipes_ns.payload
            
            # Update favorite recipe fields
            for key, value in data.items():
                if hasattr(favorite_recipe, key):
                    setattr(favorite_recipe, key, value)

            db.session.commit()
            return favorite_recipe.to_dict(), 200

        except ValueError as e:
            return {"errors": [str(e)]}, 422
        except Exception as e:
            db.session.rollback()
            return {"errors": ["An error occurred while updating the favorite recipe"]}, 500

    @jwt_required()
    @favorite_recipes_ns.doc(security='Bearer Auth')
    @favorite_recipes_ns.response(204, 'Favorite recipe removed successfully')
    @favorite_recipes_ns.response(401, 'Not authorized', error_model)
    @favorite_recipes_ns.response(404, 'Favorite recipe not found', error_model)
    def delete(self, id):
        """Remove a recipe from favorites"""
        current_user_id = get_jwt_identity()
        favorite_recipe = FavoriteRecipe.query.get_or_404(id)

        # Check if the current user owns the favorite recipe
        if favorite_recipe.user_id != current_user_id:
            return {"errors": ["Not authorized to remove this favorite recipe"]}, 401

        try:
            db.session.delete(favorite_recipe)
            db.session.commit()
            return '', 204

        except Exception as e:
            db.session.rollback()
            return {"errors": ["An error occurred while removing the recipe from favorites"]}, 500

# Register blueprint
favorite_recipes_bp = Blueprint('favorite_recipes', __name__)
