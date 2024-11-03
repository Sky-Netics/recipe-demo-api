# Tastebite Flask API

A Flask implementation of the Tastebite Recipe App API with JWT authentication and Swagger documentation.

## Features

- JWT-based authentication
- PostgreSQL database with SQLAlchemy ORM
- Interactive API documentation with Swagger UI
- Full CRUD operations for recipes and favorite recipes
- User management

## Setup and Installation

### Prerequisites
- Python 3.9+
- PostgreSQL
- pip (Python package manager)

### Local Development Setup

1. Clone the repository
2. Navigate to the flask-app directory
3. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Set up environment variables in `.env`:
```
FLASK_APP=app
FLASK_ENV=development
DATABASE_URL=postgresql://[username]:[password]@[host]:[port]/[database]
JWT_SECRET_KEY=your-secret-key
```

### Running the Application

1. Start the application:
```bash
python run.py
```

2. The API will be available at `http://localhost:5000`
3. Access the interactive API documentation at `http://localhost:5000/`

## Using the Swagger UI

1. Access the Swagger UI at `http://localhost:5000/`
2. To use protected endpoints:
   - First, create a user using the `/api/signup` endpoint or login using `/api/login`
   - Copy the `access_token` from the response
   - Click the "Authorize" button at the top of the page
   - In the authorization input field, enter: `Bearer your_access_token`
   - Click "Authorize" to save
   - Now you can use all protected endpoints

### Authentication Flow

1. Create a new user (POST /api/signup)
2. Login with credentials (POST /api/login)
3. Use the received JWT token in the Authorize button
4. Access protected endpoints

## API Endpoints

### Authentication
```
POST /api/signup
- Creates new user account
- No authentication required
- Request body: username, email, password, password_confirmation, image_url
- Returns: User object and JWT token

POST /api/login
- Authenticates user
- No authentication required
- Request body: username, password
- Returns: User object and JWT token
```

### Users
```
GET /api/users
- Lists all users
- No authentication required

GET /api/me/:id
- Gets specific user details
- Requires JWT authentication

PATCH /api/users/:id
- Updates user information
- Requires JWT authentication
- Request body: username, email, image_url (all optional)
```

### Recipes
```
GET /api/recipes
- Lists all recipes
- No authentication required

GET /api/recipes/:id
- Gets specific recipe
- No authentication required

POST /api/recipes
- Creates new recipe
- Requires JWT authentication
- Request body: title, country, rating, ingredients, procedure, 
  people_served, category, cooking_time, image_url, video_link

PATCH /api/recipes/:id
- Updates recipe
- Requires JWT authentication
- Owner only

DELETE /api/recipes/:id
- Deletes recipe
- Requires JWT authentication
- Owner only
```

### Favorite Recipes
```
GET /api/favorite_recipes
- Lists user's favorite recipes
- Requires JWT authentication
- Returns only current user's favorites

POST /api/favorite_recipes
- Adds recipe to favorites
- Requires JWT authentication
- Request body: same as recipes

PATCH /api/favorite_recipes/:id
- Updates favorite recipe
- Requires JWT authentication
- Owner only

DELETE /api/favorite_recipes/:id
- Removes recipe from favorites
- Requires JWT authentication
- Owner only
```

## Data Models

### User
- username (unique)
- email (unique)
- password (hashed)
- image_url

### Recipe
- title
- country
- rating (0-5)
- ingredients
- procedure
- people_served
- category (Breakfast/Lunch/Supper/Drinks)
- cooking_time
- image_url
- video_link
- user_id (foreign key)

### FavoriteRecipe
- Same fields as Recipe
- user_id (foreign key)

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- 200: Success
- 201: Created
- 204: No Content
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 422: Unprocessable Entity
- 500: Internal Server Error

Error responses follow the format:
```json
{
    "errors": ["Error message here"]
}
```

## Development Notes

- Database migrations are handled automatically
- JWT tokens expire after 24 hours
- All passwords are hashed using bcrypt
- CORS is enabled for all origins in development
- Interactive API documentation available at root endpoint
- Request/response validation through Flask-RESTX
- Protected endpoints require Bearer token authentication







## Folder Structure

flask-app/
├── app/                            # Main application directory
│   ├── __init__.py                # App initialization and configuration
│   ├── api_models.py              # API request/response models for Swagger
│   ├── models/                    # Database models
│   │   ├── __init__.py
│   │   ├── user.py               # User model definition
│   │   ├── recipe.py             # Recipe model definition
│   │   └── favorite_recipe.py    # FavoriteRecipe model definition
│   ├── routes/                    # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py               # Authentication endpoints (/api/signup, /api/login)
│   │   ├── users.py              # User endpoints (/api/users, /api/me)
│   │   ├── recipes.py            # Recipe CRUD endpoints
│   │   └── favorite_recipes.py   # Favorite recipes endpoints
│   └── utils/                     # Utility functions
│
├── config.py                      # Application configuration settings
├── requirements.txt               # Python dependencies
├── run.py                        # Application entry point
├── docker-compose.yml            # Docker compose configuration
└── Dockerfile                    # Docker build configuration

Key Files for Specific Functionality:
1. Authentication & User Management:
   - app/routes/auth.py
   - app/routes/users.py
   - app/models/user.py

2. Recipe Management:
   - app/routes/recipes.py
   - app/models/recipe.py

3. Favorite Recipes:
   - app/routes/favorite_recipes.py
   - app/models/favorite_recipe.py

4. API Documentation/Swagger:
   - app/api_models.py

5. Application Configuration:
   - config.py
   - docker-compose.yml

6. Database Models:
   - All files under app/models/