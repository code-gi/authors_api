from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from authors_app.extensions import db 
from authors_app.extensions import migrate,bcrypt # Removed duplicate import of Migrate
from authors_app.controllers.auth_controller import auth
from authors_app.controllers.book_controllers import book

def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    
     
    # Use Migrate from flask_migrate to initialize migrations

    # Importing and registering models
    from authors_app.models.user import User
    from authors_app.models.company import Company
    from authors_app.models.book import Books
    

    @app.route('/')
    def home():
        return "hello world"
    
    app.register_blueprint(auth,url_prefix='/api/vl/auth')
    app.register_blueprint(book,url_prefix='/api/v1/book')
    

    return app
