from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    migrate.init_app(app, db)

    # Import and initialize API
    from app.api_models import api
    
    # Create API blueprint
    api_bp = Blueprint('api', __name__)
    api.init_app(api_bp)

    # Register routes with API
    from app.routes.auth import auth_ns
    from app.routes.users import users_ns
    from app.routes.recipes import recipes_ns
    from app.routes.favorite_recipes import favorite_recipes_ns

    api.add_namespace(auth_ns, path='/api')
    api.add_namespace(users_ns, path='/api')
    api.add_namespace(recipes_ns, path='/api')
    api.add_namespace(favorite_recipes_ns, path='/api')

    # Register blueprints
    app.register_blueprint(api_bp)

    # Create database tables
    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        """Redirect root to API documentation"""
        return api.render_doc()

    return app
