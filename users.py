from db import *
from methods import *
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required, get_jwt_identity

users_bp = Blueprint('users', __name__)

# 유저 회원가입
@users_bp.route('/register', methods=['POST'])
def users_register():
    studentid = request.json.get('sid')
    name = request.json.get('name')
    contact = request.json.get('contact')
    email = request.json.get('email')
    password = request.json.get('password')
    usertype = request.json.get('usertype')

    if not studentid or not name or not contact or not email or not password:
        return jsonify({'error': 'Please provide both username and email'}), 400
    
    # Validate usertype
    if usertype not in Users_UserType_enum.__members__:
        return jsonify({'error': 'Invalid usertype'}), 401
    
    user = Users.query.filter_by(studentid = studentid).first()

    if user :
        return jsonify({'error': 'User already exists'}), 400 
    else :
        user = Users(studentid = studentid, name=name, contact=contact, email=email, usertype=Users_UserType_enum[usertype])
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()    
        return jsonify({'message': 'User registered successfully'}), 200


# 유저 로그인
@users_bp.route('/login', methods=['POST'])
def users_login():
    email = request.json.get('email')
    password = request.json.get('password')
    
    # 입력된 계정이 유효한지 확인
    user = Users.query.filter_by(email=email).first()
    
    if not user or not user.check_password(password) :
        return jsonify({'error': 'Invalid email or password'}), 400

    # 입력된 계정이 블랙리스트에 있으면 로그인 차단
    black = Blacklist.query.filter_by(userid=user.userid).first()
    if black :
        return jsonify({'error': 'Contact to admin'}), 400

    # 로그인 성공 : JWT 발급
    access_token = create_access_token(identity=user.userid)
    return jsonify({'jwt_token' : access_token}), 200

