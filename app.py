from flask import Flask, request, jsonify
import secrets
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from db import *

app = Flask(__name__)

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

# 회원가입
@app.route('/register', methods=['POST'])
def register():
    
    sid = request.json.get('sid')
    name = request.json.get('name')
    phone = request.json.get('phone')
    email = request.json.get('email')
    password = request.json.get('password')
    usertype = request.json.get('usertype')

    if not sid or not name or not phone or not email or not password:
        return jsonify({'error': 'Please provide both username and email'}), 400
    
    user = User.query.filter_by(email=email).first()

    if user :
        return jsonify({'error': 'User already exists'}), 400
    else :
        user = User(sid = sid, name=name, phone=phone, email=email,roll=roll)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()    
        return jsonify({'message': 'User registered successfully'}), 200


# 로그인
@app.route('/login', methods=['POST'])
def login():
    email = reqest.json.get('email')
    password = request.json.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not user.check_password(password) :
        return jsonify({'error': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=user.uid)
    return jsonify(access_token=access_token), 200


# 로그인 이후

# 현재 로그인 유저 이름 확인
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_uid = get_jwt_identity()
    user = User.query.filter_by(uid=current_uid).first()
    
    if not user :
        return jsonify({'error': 'User not found'}), 404

    return jsonify(login_uid=user.name), 200


# 친구 조회
@app.route('/friends', methods=['GET'])
@jwt_required()
def friends():
    current_uid = get_jwt_identity()
    friends = Friends.query.filter_by(uid1=current_uid).all()
    
    if not friends:
        return jsonify({'error': 'No friends found for this user'}), 404

    friends_list = []

    for friend in friends :
        friend_row = User.query.filter_by(uid = friend.uid2)
        if friend_row :
            friend_data = {
                'sid': friend_row.sid,
                'name': friend_row.name,
                'phone': friend_row.phone,
                'email': friend_row.email,
                'usertype': friend_row.usertype
            }
            friends_list.append(friend_data)
    return jsonify(friends=friends_list), 200


# 친구 신청 요청




# 친구 신청 수락



if __name__ == '__main__':
    app.run(debug=True)
