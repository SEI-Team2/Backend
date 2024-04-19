from db import *
from methods import *
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required, get_jwt_identity

admins_bp = Blueprint('admins', __name__)

# pending rentals 조회
@admins_bp.route('/rentals/pending', methods=['GET'])
def admins_rentals_pending():
    data = request.json
    spaceid = data.get('spaceid')

    pending_rentals = Rentals.query.filter(Rentals.spaceid==spaceid,Rentals.status == Rentals_Status_enum.Pending).all()

    if not pending_rentals:
        return jsonify({'error': 'no rentals in pending'}), 404

    rentals_data = []
    for rental in pending_rentals:
        rentals_data.append({
            'rentalid': rental.rentalid,
            'spaceid': rental.spaceid,
            'userid': rental.userid,
            'starttime': rental.starttime.strftime('%Y-%m-%d %H:%M:%S'),
            'endtime': rental.endtime.strftime('%Y-%m-%d %H:%M:%S'),
            'createtime': rental.createtime.strftime('%Y-%m-%d %H:%M:%S'),
            'status': rental.status,
            'minpeoplemet': rental.minpeoplemet
        })

    return jsonify(rentals_data), 200

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

# pending Rentals 수락
@admins_bp.route('/rentals/confirm', methods=['POST'])
def admins_rentals_confirm():
    data = request.json
    
    # TODO : 현재 유저가 관리자인지 확인
    # TODO : Rentals 에서 해당 Rental status 를 confirmed 로 변경
    #      : confirmed 로 바뀐 후, 참여자들에게 공지

# pending ClubTimeSlot 수락
@admins_bp.route('/clubtimeslots/confirm', methods=['POST'])
def admins_clubtimeslots_confirm():
    data = request.json
    
    # TODO : 현재 유저가 관리자인지 확인
    # TODO : Rentals 에서 해당 Rental status 를 confirmed 로 변경
    #      : confirmed 로 바뀐 후, 참여자들에게 공지

# 예약 불가능한 시간에 대한 등록
@admins_bp.route('/cancle', methods=['POST'])
def admins_cancel():
    data = request.json
    
    # TODO : 특정 일정에 대한 취소


