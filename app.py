from flask import Flask, request, jsonify
from db import *

app = Flask(__name__)

# Configure database connection URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'

# Initialize SQLAlchemy
db.init_app(app)

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
    roll = request.json.get('roll') # need handling

    if not sid or not name or not phone or not email:
        return jsonify({'error': 'Please provide both username and email'}), 400
    
    user = User.query.filter_by(sid=sid).first()

    if user :
        return jsonify({'error': 'User already exists'}), 400
    else :
        user = User(sid = sid, name=name, phone=phone, email=email,roll=roll)
        db.session.add(user)
        db.session.commit()    
        return jsonify({'message': 'User registered successfully'}), 200


# 로그인
@app.route('/login', methods=['GET'])
def login():
    users = User.query.all()
    result = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
