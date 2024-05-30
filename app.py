from flask import Flask, request, jsonify
import secrets
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from db import *
from datetime import datetime, timedelta

from rentals import rentals_bp
from friends import friends_bp
from notifications import notifications_bp
from users import users_bp
from profiles import profiles_bp
from schedules import schedules_bp

app = Flask(__name__)
app.register_blueprint(rentals_bp, url_prefix='/rentals')
app.register_blueprint(friends_bp, url_prefix='/friends')
app.register_blueprint(notifications_bp, url_prefix='/notifications')
app.register_blueprint(profiles_bp, url_prefix='/profiles')
app.register_blueprint(schedules_bp, url_prefix='/schedules')

# App Config 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['JWT_SECRET_KEY'] = secrets.token_urlsafe(32)

# Initialize SQLAlchemy
# Initialize JWT
db.init_app(app)
jwt = JWTManager(app)

# Create the database
with app.app_context():
    db.create_all()

# Routes

if __name__ == '__main__':
    app.run(debug=True)