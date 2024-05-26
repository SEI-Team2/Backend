from db import *
from methods import *
from flask import *
from datetime import *
from flask_jwt_extended import *

admins_bp = Blueprint('admins', __name__)

# 동아리 관리자 임명
# TODO for frontend :
# 1. jwt 토큰 + studentid + clubname
# 2. 지명 유저를 동아리 관리자로 갱신 (Users, Clubmembers)
@admins_bp.route('/clubmanager/register', methods=['GET'])
@jwt_required()
def admins_clubmanager_register():
    current_userid = get_jwt_identity()
    data = request.json

    studentid = data.get('studentid')
    clubname = data.get('clubname')

    club = db.session.query(Clubs).filter_by(name == clubname).first()
    if not club :
        return jsonify({"error" : "Club not exist" }), 400
    clubid = club.clubid

    # Users.usertype 갱신
    user = db.session.query(Users).filter_by(studentid == studentid).first()
    if not user:
        return jsonify({"error" : "Studentid not exist" }), 400
    userid= user.userid
    user.usertype = Chairperson
    db.session.commit()

    # ClubMembers 갱신
    clubmember = db.session.query(Clubmembers).filter_by(userid == userid, clubid == clubid).first()
    if not clubmember :
        clubmember = ClubMembers(userid = userid, clubid = clubid, role = Manager)
        db.session.add(clubmember)
        db.session.commit()
        return jsonify({}), 200
    clubmember.role = Manager
    db.session.commit()

    return jsonify({}), 200


# pending ClubTimeSlots 조회
@admins_bp.route('/clubtimeslots/pending', methods=['GET'])
def admins_clubtimeslots_pending():
    data = request.json
    spaceid = data.get('spaceid')

    pending_clubtimeslots = ClubTimeSlots.query.filter(ClubTimeSlots.spaceid==spaceid, ClubTimeSlots.status == ClubTimeSlots_Status_enum.Pending).all()

    if not pending_clubtimeslots:
        return jsonify({'error': 'no rentals in pending'}), 404

    clubtimeslots_data = []
    for clubtimeslot in pending_clubtimeslots:
        clubtimeslots_data.append({
            'slotid': clubtimeslot.slotid,
            'spaceid': clubtimeslot.spaceid,
            'clubid': clubtimeslot.clubid,
            'starttime': clubtimeslot.starttime.strftime('%Y-%m-%d %H:%M:%S'),
            'endtime': clubtimeslot.endtime.strftime('%Y-%m-%d %H:%M:%S'),
            'status': clubtimeslot.status,
            'minpeoplemet': clubtimeslot.minpeoplemet
        })

    return jsonify(clubtimeslots_data), 200

# pending Rentals 거절
@admins_bp.route('/rentals/reject', methods=['POST'])
def admins_rentals_reject():
    data = request.json
    
    # TODO : 현재 유저가 관리자인지 확인
    #      : Rentals 에서 해당 Rental status 를 rejected 로 변경
    #      : rejected 로 바뀐 후, 참여자들에게 공지

# pending ClubTimeSlot 거절
@admins_bp.route('/clubtimeslots/reject', methods=['POST'])
def admins_clubtimeslots_reject():
    data = request.json
    
    # TODO : 현재 유저가 관리자인지 확인
    # TODO : Rentals 에서 해당 Rental status 를 rejected 로 변경
    #      : rejected 로 바뀐 후, 참여자들에게 공지

# 예약 불가능한 시간에 대한 등록
@admins_bp.route('/cancle', methods=['POST'])
def admins_cancel():
    data = request.json
    
    # TODO : 특정 일정에 대한 취소


