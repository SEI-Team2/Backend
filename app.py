from flask import Flask, request, jsonify
import secrets
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from db import *
from datetime import datetime, timedelta
from rentals import rentals_bp
from friends import friends_bp
from admins import admins_bp
from clubtimeslots import clubtimeslots_bp

app = Flask(__name__)
app.register_blueprint(rentals_bp, url_prefix='/rentals')
app.register_blueprint(friends_bp, url_prefix='/friends')
app.register_blueprint(admins_bp, url_prefix='/admins')
app.register_blueprint(clubtimeslots_bp, url_prefix='/clubtimeslots')

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