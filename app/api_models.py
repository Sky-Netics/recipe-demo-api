from flask_restx import Api, fields

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Type in the *\'Value\'* input box below: **\'Bearer &lt;JWT&gt;\'**, where JWT is the token'
    },
}

api = Api(
    title='Tastebite API',
    version='1.0',
    description='A recipe management API',
    authorizations=authorizations,
    security='Bearer Auth'  # Set default security
)

# User models
user_input = api.model('UserInput', {
    'username': fields.String(required=True, description='User username'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'password_confirmation': fields.String(required=True, description='Password confirmation'),
    'image_url': fields.String(required=True, description='User profile image URL'),
    'role': fields.String(required=False, description='User role (admin/user)', default='user')
})

user_output = api.model('User', {
    'id': fields.Integer(description='User ID'),
    'username': fields.String(description='User username'),
    'email': fields.String(description='User email'),
    'image_url': fields.String(description='User profile image URL'),
    'role': fields.String(description='User role')
})

login_input = api.model('LoginInput', {
    'username': fields.String(required=True, description='User username'),
    'password': fields.String(required=True, description='User password')
})

auth_response = api.model('AuthResponse', {
    'user': fields.Nested(user_output),
    'access_token': fields.String(description='JWT access token')
})

# Recipe models
recipe_input = api.model('RecipeInput', {
    'title': fields.String(required=True, description='Recipe title'),
    'country': fields.String(required=True, description='Country of origin'),
    'rating': fields.Float(required=True, description='Recipe rating (0-5)'),
    'ingredients': fields.String(required=True, description='Recipe ingredients'),
    'procedure': fields.String(required=True, description='Cooking procedure'),
    'people_served': fields.Integer(required=True, description='Number of people served'),
    'category': fields.String(required=True, description='Recipe category (Breakfast/Lunch/Supper/Drinks)'),
    'cooking_time': fields.String(required=True, description='Cooking time'),
    'image_url': fields.String(required=True, description='Recipe image URL'),
    'video_link': fields.String(required=True, description='Recipe video link')
})

recipe_output = api.model('Recipe', {
    'id': fields.Integer(description='Recipe ID'),
    'title': fields.String(description='Recipe title'),
    'country': fields.String(description='Country of origin'),
    'rating': fields.Float(description='Recipe rating'),
    'ingredients': fields.String(description='Recipe ingredients'),
    'procedure': fields.String(description='Cooking procedure'),
    'people_served': fields.Integer(description='Number of people served'),
    'category': fields.String(description='Recipe category'),
    'cooking_time': fields.String(description='Cooking time'),
    'image_url': fields.String(description='Recipe image URL'),
    'video_link': fields.String(description='Recipe video link'),
    'user_id': fields.Integer(description='User ID who created the recipe'),
    'user': fields.String(description='Username who created the recipe')
})

# Error models
error_model = api.model('Error', {
    'errors': fields.List(fields.String, description='List of error messages')
})
