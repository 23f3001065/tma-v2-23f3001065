from flask import Flask
from flask_cors import CORS

from routes import admin, auth, staff, trekker
from config import Config
from extensions import db, api, jwt, mail, cache

from datetime import date


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

def create_sample_treks():

    from models.trek import Trek

    if Trek.query.first():
        return

    trek1 = Trek(
        name="Valley Trek",
        location="Himachal Pradesh",
        difficulty="Easy",
        duration_days=3,
        description="Beautiful valley trek",
        available_slots=25,
        start_date=date(2026, 9, 1),
        end_date=date(2026, 9, 3),
        status="Open"
    )

    trek2 = Trek(
        name="Snow Peak Trek",
        location="Kashmir",
        difficulty="Hard",
        duration_days=5,
        description="Snow covered mountain trek",
        available_slots=15,
        start_date=date(2026, 9, 10),
        end_date=date(2026, 9, 14),
        status="Open"
    )

    db.session.add(trek1)
    db.session.add(trek2)

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

    mail.init_app(app)
    cache.init_app(app)
    
    # register_routes(app)
    register_routes()
    
    with app.app_context():
        db.create_all()

        create_admin_user()
        create_sample_treks()
    
    return app