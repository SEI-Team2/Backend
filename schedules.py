from db import *
from methods import *
from flask import *
from datetime import *
from flask_jwt_extended import *

schedules_bp = Blueprint('schedules', __name__)

# 스케쥴 조회
@schedules_bp.route('/list', methods=['GET'])
@jwt_required()
def schedules_list():
    methods_update_rentals()
    spaceid = data.get('spaceid')
    date_str = data.get('date')

    if not spaceid or not date_str:
        return jsonify({'error': 'Space ID and date are required'}), 400

    if not (0 <= spaceid <= 2) :
        return jsonify({'error': 'Space ID is invalid'}), 400

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format, should be YYYY-MM-DD'}), 400

    start_of_day = datetime.combine(date, datetime.min.time())
    end_of_day = datetime.combine(date, datetime.max.time())

    rentals = db.session.query(Rentals).filter(
        Rentals.spaceid == spaceid,
        Rentals.starttime >= start_of_day,
        Rentals.endtime <= end_of_day,
    ).all()

    rentals_list = []
    for rental in rentals :
        name = "번개모임"
        if rental.rentaltype == Rentals_Types_enum.Club :
            club = db.session.query(Clubs).filter(Clubs.clubid == rental.clubid).first()
            if club :
                name = club.name
        elif rental.rentaltype == Rentals_Types_enum.Restrict :
            name = "관리자제한" 
        rentals_list.append({
            'rentalid': rental.rentalid,
            'spaceid': rental.spaceid,
            'userid': rental.userid,

            'name' : name,
            
            'starttime': rental.starttime.strftime('%Y-%m-%d %H:%M:%S'),
            'endtime': rental.endtime.strftime('%Y-%m-%d %H:%M:%S'),
            'createtime': rental.createtime.strftime('%Y-%m-%d %H:%M:%S'),
              
            'maxpeople': rental.maxpeople,
            'minpeople': rental.minpeople,
            'people': rental.people,
            
            'rentaltype' : rental.rentaltype.name,
            'rentalstatus': rental.rentalstatus.name,
            'rentalflag': rental.rentalflag.name,

            'desc' : rental.desc,
        })

    return jsonify({'schedules':rentals_list}), 200

