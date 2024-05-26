from db import *
from methods import *
from flask import *
from datetime import *
from flask_jwt_extended import *

friends_bp = Blueprint('friends', __name__)

# 친구 목록 조회
# TODO for frontend :
# 1. jwt 토큰으로 해당 경로로 요청합니다.
# 2. 현재 유저의 모든 친구 {name, contact, email} 들을 반환합니다.
@friends_bp.route('/list', methods=['GET'])
@jwt_required()
def friends_list():
    current_userid = get_jwt_identity()
    data = request.json

    friends1 = Friends.query.filter_by(Friends.userid1 == current_userid, Friends.status == Accepted).all()
    friends2 = Friends.query.filter_by(Friends.userid2 == current_userid, Friends.status == Accepted).all()

    friends_id = set()
    for friend1 in friends1 :
        friends_id.add(friend1.userid2)
    for friend2 in friends2 :
        friends_id.add(friend1.userid1)
    
    friends = []
    for friend_id in friends_id :
        user = Users.query.filter_by(Users.userid == friend_id).first()
        friends.append({
            'name' : user.name,
            'studentid' : user.studentid,
            'contact': user.contact,
            'email' : user.email,
        })
    return jsonify(friends), 200


# 받은 친구 요청 목록 조회
# TODO for frontend :
# 1. jwt 토큰으로 해당 경로로 요청합니다.
# 2. 현재 유저가 받은 친구 요청의 발신자 정보 {name, contact, email} 들을 반환합니다.
@friends_bp.route('/reqeusts/receive', methods=['GET'])
@jwt_required()
def friends_requests_receive():
    current_userid = get_jwt_identity()
    data = request.json
    
    requests = Friends.query.filter_by(Friends.userid2 == current_userid, Friends.status == Pending).all()
    
    requests_data = []
    for request in requests :
        user = Users.query.filter_by(Users.userid == request.userid1).first()
        requests_data.append({
            'name' : user.name,
            'studentid' : user.studentid,
            'contact': user.contact,
            'email' : user.email,
        })
    return jsonify(requests_data), 200


# 받은 친구 요청 수락
# TODO for frontend :
# 1. jwt 토큰 + studentid
# 2. 받은 친구 신청에 대한 수락 처리
@friends_bp.route('/reqeusts/receive/accept', methods=['GET'])
@jwt_required()
def friends_requests_receive_accept():
    current_userid = get_jwt_identity()
    data = request.json
    studentid = data.get('studentid')

    user = Users.query.filter_by(Users.studentid == studentid).first()
    if not user :
            return jsonify({"error" : "Studentid not exist" }), 400
    userid = user.userid

    request = db.session.query(Friends).filter_by(userid1 == userid, userid2 == current_userid, status == Pending).first()
    if not request:
        return jsonify({"error" : "Request not exist" }), 400
    request.status = Accepted

    db.session.commit()

    # 알림 생성 : 친구요청 발신자에게 요청 수락 알림
    current_user = Users.query.filter_by(Users.userid == current_userid).first()
    notification = Notifications(userid = userid, msg = current_user.name +" 이 친구 요청을 수락했습니다!", timestamp = datetime.utcnow ,status = Unread )
    db.session.add(notification)
    db.session.commit()
    # 알림 생성

    return jsonify({}), 200


# 받은 친구 요청 거절
# TODO for frontend :
# 1. jwt 토큰 + studentid
# 2. 받은 친구 신청에 대한 거절 처리
@friends_bp.route('/reqeusts/receive/reject', methods=['GET'])
@jwt_required()
def friends_requests_receive_reject():
    current_userid = get_jwt_identity()
    data = request.json
    studentid = data.get('studentid')

    user = Users.query.filter_by(Users.studentid == studentid).first()
    if not user :
            return jsonify({"error" : "Studentid not exist" }), 400
    userid = user.userid

    request = db.session.query(Friends).filter_by(userid1 == userid, userid2 == current_userid, status == Pending).first()
    if not request:
        return jsonify({"error" : "Request not exist" }), 400
    request.status = Rejected

    db.session.commit()

    return jsonify({}), 200


# 보낸 친구 요청 목록 조회
# TODO for frontend :
# 1. jwt 토큰으로 해당 경로로 요청합니다.
# 2. 현재 유저가 보낸 친구 요청의 수신자 정보 {name, contact, email} 들을 반환합니다.
@friends_bp.route('/reqeusts/send', methods=['GET'])
@jwt_required()
def friends_requests_send():
    current_userid = get_jwt_identity()
    data = request.json
    
    requests = Friends.query.filter_by(Friends.userid1 == current_userid, Friends.status == Pending).all()
    
    requests_data = []
    for request in requests :
        user = Users.query.filter_by(Users.userid == request.userid2).first()
        requests_data.append({
            'name' : user.name,
            'studentid' : user.studentid,
            'contact': user.contact,
            'email' : user.email,
        })
    return jsonify(requests_data), 200


# 보낸 친구 요청 목록 취소
# TODO for frontend :
# 1. jwt 토큰 + studentid 
# 2. 보낸 친구 요청 취소
@friends_bp.route('/reqeusts/cancle', methods=['GET'])
@jwt_required()
def friends_requests_cancle():
    current_userid = get_jwt_identity()
    data = request.json
    studentid = data.get('studentid')

    user = Users.query.filter_by(Users.studentid == studentid ).first()
    if not user :
        return jsonify({'error' : "Studentid not exist" }), 400 
    userid = user.userid

    deletion_results = []

    rows_deleted = db.session.query(Friends).filter_by(userid1==current_userid, userid2==userid, status == Pending).delete()
    deletion_results.append((userid1, userid2, rows_deleted))

    db.session.commit()

    for userid1, userid2, rows_deleted in deletion_results:
        if rows_deleted > 0:
            return jsonify({}), 200 
        else:
            return jsonify({'error' : "Request not exist" }), 400 


# 친구 요청 
# TODO for frontend :
# 1. jwt 토큰 + ('studentid') 으로 해당 경로로 요청합니다.
@friends_bp.route('/reqeusts', methods=['GET'])
@jwt_required()
def friends_requests():
    current_userid = get_jwt_identity()
    data = request.json
    studentid = data.get('studentid')
    
    user = Users.query.filter_by(Users.studentid == studentid).first()
    if not user :
        return jsonify({'error' : "Studentid not exist" }), 400 
    userid = user.userid

    already = Friends.query.filter_by(Friends.userid1 == current_userid, Friends.userid2 == userid).all()
    if already :
        return jsonify({'error' : "Already requested" }), 400   

    friend = Friends(Friends.userid1 = current_userid, Friends.userid2 = userid, Friends.status = Pending)
    
    db.session.add(friend)
    db.session.commit()

    # 알림 생성 : 친구요청 수신자에게 요청 수신 알림
    current_user = Users.query.filter_by(Users.userid == current_userid).first()
    notification = Notifications(userid = userid, msg = current_user.name +" 으로 부터 친구 요청이 도착했습니다!", timestamp = datetime.utcnow ,status = Unread )
    db.session.add(notification)
    db.session.commit()
    # 알림 생성

    return jsonify({}), 200



