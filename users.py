from db import *
from methods import *
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required, get_jwt_identity

users_bp = Blueprint('users', __name__)

# user register
@users_bp.route('/users/register', methods=['POST'])
def register():
    studentid = request.json.get('sid')
    name = request.json.get('name')
    contract = request.json.get('contract')
    email = request.json.get('email')
    password = request.json.get('password')
    usertype = request.json.get('usertype')

    if not studentid or not name or not contract or not email or not password:
        return jsonify({'error': 'Please provide both username and email'}), 400
    
    user = User.query.filter_by(email=email).first()

    if user :
        return jsonify({'error': 'User already exists'}), 400
    else :
        user = User(studentid = studentid, name=name, contract=contract, email=email,usertype=usertype)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()    
        return jsonify({'message': 'User registered successfully'}), 200

# user login
@users_bp.route('/users/login', methods=['POST'])
def login():
    email = reqest.json.get('email')
    password = request.json.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not user.check_password(password) :
        return jsonify({'error': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=user.userid)
    return jsonify(access_token=access_token), 200

# user porfile
@users_bp.route('/users/profile', methods=['GET'])
@jwt_required()
def profile():
    current_userid = get_jwt_identity()
    user = User.query.filter_by(userid1=current_userid).first()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify(name = user.name,studentid = user.studentid,email=user.email), 200

