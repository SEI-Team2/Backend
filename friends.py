from db import *
from methods import *
from flask import *
from datetime import *
from flask_jwt_extended import *

friends_bp = Blueprint('friends', __name__)

# 친구 목록 조회
@friends_bp.route('/list', methods=['GET'])
@jwt_required()
def friends_list():
    current_userid = get_jwt_identity()

    friends1 = db.session.query(Friends).filter(Friends.userid1 == current_userid, Friends.status == Friends_Status_enum.Accepted).all()
    friends2 = db.session.query(Friends).filter(Friends.userid2 == current_userid, Friends.status == Friends_Status_enum.Accepted).all()

    friends_id = set()
    for friend1 in friends1 :
        friends_id.add(friend1.userid2)
    for friend2 in friends2 :
        friends_id.add(friend2.userid1)
    
    friends = []
    for friend_id in friends_id :
        user = db.session.query(Users).filter(Users.userid == friend_id).first()
        if not user :
            continue
        friends.append({
            'userid' : user.userid,
            'name' : user.name,
            'studentid' : user.studentid,
            'contact': user.contact,
            'email' : user.email,
        })

    return jsonify({'friends' : friends}), 200


# 받은 친구 요청 목록 조회
@friends_bp.route('/requests/receive', methods=['GET'])
@jwt_required()
def friends_requests_receive():
    current_userid = get_jwt_identity()
    
    friends = db.session.query(Friends).filter(Friends.userid2 == current_userid, Friends.status == Friends_Status_enum.Pending).all()
    
    friends_data = []
    for friend in friends :
        user = db.session.query(Users).filter(Users.userid == friend.userid1).first()
        if not user :
            continue
        friends_data.append({
            'userid' : user.userid,
            'name' : user.name,
            'studentid' : user.studentid,
            'contact': user.contact,
            'email' : user.email,
        })

    return jsonify({'requests' : friends_data}), 200


# 받은 친구 요청 수락
@friends_bp.route('/requests/receive/accept', methods=['POST'])
@jwt_required()
def friends_requests_receive_accept():
    current_userid = get_jwt_identity()
    data = request.json

    studentid = data.get('studentid')

    user = db.session.query(Users).filter(Users.studentid == studentid).first()
    if not user :
            return jsonify({"error" : "Studentid not exist" }), 400

    friend = db.session.query(Friends).filter(Friends.userid1 == user.userid, Friends.userid2 == current_userid, Friends.status == Friends_Status_enum.Pending).first()
    if not friend:
        return jsonify({"error" : "Request not exist" }), 401
    friend.status = Friends_Status_enum.Accepted

    # 알림 #
    notify = Notifications(userid=user.userid, notifytype=Notifications_Types_enum.friend_accept, friendid=current_userid)
    db.session.add(notify)
    # 알림 #

    db.session.commit()

    return jsonify({}), 200


# 받은 친구 요청 거절
@friends_bp.route('/requests/receive/reject', methods=['POST'])
@jwt_required()
def friends_requests_receive_reject():
    current_userid = get_jwt_identity()
    data = request.json

    studentid = data.get('studentid')

    user = db.session.query(Users).filter(Users.studentid == studentid).first()
    if not user :
            return jsonify({"error" : "Studentid not exist" }), 401

    friend = db.session.query(Friends).filter(Friends.userid1 == user.userid, Friends.userid2 == current_userid, Friends.status == Friends_Status_enum.Pending).first()
    if not friend:
        return jsonify({"error" : "Request not exist" }), 402
    friend.status = Friends_Status_enum.Rejected

    # 알림 #
    notify = Notifications(userid=user.userid, notifytype=Notifications_Types_enum.friend_reject, friendid=current_userid)
    db.session.add(notify)
    # 알림 #
    
    db.session.commit()

    return jsonify({}), 200


# 보낸 친구 요청 목록 조회
@friends_bp.route('/requests/send', methods=['POST'])
@jwt_required()
def friends_requests_send():
    current_userid = get_jwt_identity()
    
    friends = db.session.query(Friends).filter(Friends.userid1 == current_userid, Friends.status != Friends_Status_enum.Accepted).all()
    
    friends_data = []
    for friend in friends :
        user = db.session.query(Users).filter(Users.userid == friend.userid2).first()
        if not user :
            continue
        friends_data.append({
            'status' : friend.status.name,
            'userid' : user.userid,
            'name' : user.name,
            'studentid' : user.studentid,
            'contact': user.contact,
            'email' : user.email,
        })
    return jsonify({'requests' : friends_data}), 200


# 보낸 친구 요청 목록 취소
@friends_bp.route('/requests/cancle', methods=['POST'])
@jwt_required()
def friends_requests_cancle():
    current_userid = get_jwt_identity()
    data = request.json

    studentid = data.get('studentid')

    user = db.session.query(Users).filter(Users.studentid == studentid).first()
    if not user :
        return jsonify({'error' : "Studentid not exist" }), 400 

    friend = db.session.query(Friends).filter(Friends.userid1 == current_userid, Friends.userid2 == user.userid, Friends.status != Friends_Status_enum.Accepted).first()
    if not friend :
        return jsonify({'error' : "request not exist" }), 400
    
    db.session.delete(friend)
    
    db.session.commit()

    return jsonify({}), 200


# 친구 요청
@friends_bp.route('/requests', methods=['POST'])
@jwt_required()
def friends_requests():
    current_userid = get_jwt_identity()
    data = request.json

    studentid = data.get('studentid')
    
    user = db.session.query(Users).filter(Users.studentid == studentid).first()
    if not user :
        return jsonify({'error' : "Studentid not exist" }), 401

    already = db.session.query(Friends).filter(Friends.userid1 == current_userid, Friends.userid2 == user.userid).first()
    if already :
        return jsonify({'error' : "Already requested" }), 402   

    friend = Friends(userid1 = current_userid, userid2 = user.userid, status = Friends_Status_enum.Pending)
    db.session.add(friend)
    db.session.commit()

    # 알림 #
    notify = Notifications(userid = user.userid, notifytype=Notifications_Types_enum.friend_request, friendid = current_userid)
    db.session.add(notify)
    # 알림 #

    db.session.commit()

    return jsonify({}), 200

# 친구 삭제
@friends_bp.route('/delete', methods=['POST'])
@jwt_required()
def friends_delete():
    current_userid = get_jwt_identity()
    data = request.json

    studentid = data.get('studentid')

    user = db.session.query(Users).filter(Users.studentid == studentid).first()
    if not user :
        return jsonify({'error' : "Studentid not exist" }), 400

    friend = (
        db.session.query(Friends)
        .filter(
            or_(
                and_(Friends.userid1 == current_userid, Friends.userid2 == user.userid),
                and_(Friends.userid1 == user.userid, Friends.userid2 == current_userid),
            ),
            Friends.status == Friends_Status_enum.Accepted,
        )
        .first()
    )
    if not friend :
        return jsonify({'error' : "Friend not exist" }), 401

    db.session.delete(friend)
    db.session.commit()

    return jsonify({}), 200
