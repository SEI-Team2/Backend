from db import *
from methods import *
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required, get_jwt_identity

clubtimeslots_bp = Blueprint('clubtimeslots', __name__)

# 동아리 예약 일정 조회(주 단위)
@clubtimeslots_bp.route('/week', methods=['GET'])
def clubtimeslots_week():
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

# 동아리 예약 일정 조회(일 단위)
@clubtimeslots_bp.route('/day', methods=['GET'])
def clubtimeslots_day():
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


# 동아리 예약 일정 참여
@clubtimeslots_bp.route('/join', methods=['POST'])
def clubtimeslots_join():
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

    
