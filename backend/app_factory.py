from flask import Flask
from flask_cors import CORS

from routes import admin, auth, staff, trekker
from config import Config
from extensions import db, api, jwt


def create_admin_user():
    from models.user import User
    
    admin = User.query.filter_by(email="admin@gmail.com").first()
    
    if not admin:
        admin = User(
            name="Admin",
            email="admin@gmail.com",
            password="admin",
            role="admin",
            is_active=True
        )
        db.session.add(admin)
        db.session.commit()

def register_routes():
    pass

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    api.init_app(app)
    jwt.init_app(app)
    
    # register_routes(app)
    register_routes()
    
    with app.app_context():
        db.create_all()
        create_admin_user()
    
    return app