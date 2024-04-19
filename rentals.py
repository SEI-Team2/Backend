from db import *
from methods import *
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required, get_jwt_identity

rentals_bp = Blueprint('rentals', __name__)


# 렌탈 일정 신청
# 특정 시간의 렌탈 일정 추가
@rentals_bp.route('/create', methods=['POST'])
def rentals_create():

    data = request.json
    spaceid = data.get('spaceid')
    starttime = data.get('starttime')
    endtime = data.get('endtime')
    curtime = datetime.utcnow

    # TODO : Rentals, ClubTimeslot, 조교 재량 시간?? 에 대한 체크 수행 후 가능하면 추가.
    
    
# 렌탈 일정 조회(주 단위)
@rentals_bp.route('/week', methods=['GET'])
def rentals_week():
    data = request.json
    spaceid = data.get('spaceid')
    week = data.get('week')

    week_start = datetime.strptime(week, '%Y-%m-%d')

    week_end = week_start + timedelta(days=7)

    rentals_in_week = Rentals.query.filter(Rentals.spaceid==spaceid,Rentals.starttime >= week_start, Rentals.starttime < week_end).all()

    if not rentals_in_week:
        return jsonify({'error': 'no rentals in the week'}), 404

    rentals_data = []
    for rental in rentals_in_week:
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

# 렌탈 일정 조회(일 단위)
@rentals_bp.route('/day', methods=['GET'])
def rentals_day():
    data = request.json
    spaceid = data.get('spaceid')
    day = data.get('day')

    day_start = datetime.strptime(day, '%Y-%m-%d')

    day_end = day_start + timedelta(days=1)

    rentals_in_day = Rentals.query.filter(Rentals.spaceid==spaceid,Rentals.starttime >= day_start, Rentals.starttime < day_end).all()

    if not rentals_in_day:
        return jsonify({'error': 'no rentals in the week'}), 404

    rentals_data = []
    for rental in rentals_in_day:
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


# 렌탈 일정 참가
@rentals_bp.route('/join', methods=['GET'])
def rentals_join():
    data = request.json
    rentalid = data.get('rentalid')
    userid = data.get('userid')

    # TODO : Rentals 의 status 를 통해 참여 가능한지 확인하고, 가능한 경우 RentalParticipants 에 등록
    
