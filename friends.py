from db import *
from methods import *
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required, get_jwt_identity

friends_bp = Blueprint('friends', __name__)

# 받은 친구 요청 목록 
@friends_bp.route('/reqeusts/pending', methods=['POST'])
def friedns_requests_pending():
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

# 보낸 친구 요청 목록 
@friends_bp.route('/reqeusts/sending', methods=['POST'])
def friends_requests_sending():
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

# 친구 목록 
@friends_bp.route('/list', methods=['POST'])
def friends_list():
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




