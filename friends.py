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
@friends_bp.route('/list', methods=['POST'])
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
            'userid' : user.userid,
            'name' : user.name,
            'studentid' : user.studentid,
            'contact': user.contact,
            'email' : user.email,
        })

    return jsonify({'friends' : friends}), 200


# 받은 친구 요청 목록 조회
# TODO for frontend :
# 1. jwt 토큰으로 해당 경로로 요청합니다.
# 2. 현재 유저가 받은 친구 요청의 발신자 정보 {name, contact, email} 들을 반환합니다.
@friends_bp.route('/reqeusts/receive', methods=['POST'])
@jwt_required()
def friends_requests_receive():
    current_userid = get_jwt_identity()
    data = request.json
    
    requests = Friends.query.filter_by(Friends.userid2 == current_userid, Friends.status == Pending).all()
    
    requests_data = []
    for request in requests :
        user = Users.query.filter_by(Users.userid == request.userid1).first()
        requests_data.append({
            'userid' : user.userid,
            'name' : user.name,
            'studentid' : user.studentid,
            'contact': user.contact,
            'email' : user.email,
        })

    return jsonify({'requests' : requests_data}), 200


# 받은 친구 요청 수락
@friends_bp.route('/reqeusts/receive/accept', methods=['POST'])
@jwt_required()
def friends_requests_receive_accept():
    current_userid = get_jwt_identity()
    data = request.json

    studentid = data.get('studentid')

    user = Users.query.filter_by(Users.studentid == studentid).first()
    if not user :
            return jsonify({"error" : "Studentid not exist" }), 400

    request = db.session.query(Friends).filter_by(Friends.userid1 == user.userid, Friends.userid2 == current_userid, Friends.status == Pending).first()
    if not request:
        return jsonify({"error" : "Request not exist" }), 400
    request.status = Friends_Status_enum.Accepted

    # 알림 #
    notify = Notifications(userid=user.userid, notifytype=Notifications_Types_enum.friend_accept, friendid=current_userid)
    db.session.add(notify)
    # 알림 #

    db.session.commit()

    return jsonify({}), 200


# 받은 친구 요청 거절
# TODO for frontend :
# 1. jwt 토큰 + studentid
# 2. 받은 친구 신청에 대한 거절 처리
@friends_bp.route('/reqeusts/receive/reject', methods=['POST'])
@jwt_required()
def friends_requests_receive_reject():
    current_userid = get_jwt_identity()
    data = request.json

    studentid = data.get('studentid')

    user = Users.query.filter_by(Users.studentid == studentid).first()
    if not user :
            return jsonify({"error" : "Studentid not exist" }), 400

    request = db.session.query(Friends).filter_by(Friends.userid1 == user.userid, Friends.userid2 == current_userid, Friends.status == Pending).first()
    if not request:
        return jsonify({"error" : "Request not exist" }), 400
    request.status = Friends_Status_enum.Rejected

    # 알림 #
    notify = Notifications(userid=user.userid, notifytype=Notifications_Types_enum.friend_reject, friendid=current_userid)
    db.session.add(notify)
    # 알림 #
    
    db.session.commit()

    return jsonify({}), 200


# 보낸 친구 요청 목록 조회
# TODO for frontend :
# 1. jwt 토큰으로 해당 경로로 요청합니다.
# 2. 현재 유저가 보낸 친구 요청의 수신자 정보 {name, contact, email} 들을 반환합니다.
@friends_bp.route('/reqeusts/send', methods=['POST'])
@jwt_required()
def friends_requests_send():
    current_userid = get_jwt_identity()
    data = request.json
    
    requests = Friends.query.filter_by(Friends.userid1 == current_userid, Friends.status != Friends_Status_enum.Accepted).all()
    
    requests_data = []
    for request in requests :
        user = Users.query.filter_by(Users.userid == request.userid2).first()
        requests_data.append({
            'status' : request.status.name,
            'userid' : user.userid,
            'name' : user.name,
            'studentid' : user.studentid,
            'contact': user.contact,
            'email' : user.email,
        })
    return jsonify({'requests' : requests_data}), 200


# 보낸 친구 요청 목록 취소
# TODO for frontend :
# 1. jwt 토큰 + studentid 
# 2. 보낸 친구 요청 취소
@friends_bp.route('/reqeusts/cancle', methods=['POST'])
@jwt_required()
def friends_requests_cancle():
    current_userid = get_jwt_identity()
    data = request.json

    studentid = data.get('studentid')

    user = Users.query.filter_by(Users.studentid == studentid ).first()
    if not user :
        return jsonify({'error' : "Studentid not exist" }), 400 

    request = Friends.query.filter_by(Friends.userid1 == current_userid, Friends.status == Friends_Status_enum.Pending).all()
    if not request :
        return jsonify({'error' : "request not exist" }), 400
    
    db.session.delete(request)
    
    db.session.commit()

    return 


# 친구 요청 
@friends_bp.route('/reqeusts', methods=['POST'])
@jwt_required()
def friends_requests():
    current_userid = get_jwt_identity()
    data = request.json

    studentid = data.get('studentid')
    
    user = Users.query.filter_by(Users.studentid == studentid).first()
    if not user :
        return jsonify({'error' : "Studentid not exist" }), 400 

    already = Friends.query.filter_by(Friends.userid1 == current_userid, Friends.userid2 == userid).all()
    if already :
        return jsonify({'error' : "Already requested" }), 400   

    friend = Friends(userid1 = current_userid, userid2 = userid, status = Pending)
    
    db.session.add(friend)

    # 알림 #
    current_user = Users.query.filter_by(Users.userid == current_userid).first()
    notify = Notifications(userid = user.userid, notifytype=Notifications_Types_enum.friend_request, friendid = current_userid)
    db.session.add(notify)
    # 알림 #

    db.session.commit()

    return jsonify({}), 200



