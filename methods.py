from db import *
from methods import *
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required, get_jwt_identity

# 렌탈에 대한 인원 변동시, 해당 렌탈의 status 를 갱신
def methods_update_Users_status(rentalid) :
    
    rental = Rentals.query.filter(Rentals.rentalid == rentalid).first()
    if not rental:
        return jsonify({'error': 'invalid rentalid'})

    spaceid = rental.spaceid

    sportspace = SportsSpace.query.filter(SportsSpace.spaceid == spaceid).first()
    if not sportspace:
        return jsonify({'error': 'invalid space id'})

    minpeople = sportspace.minpeople

    rentalpeople = RentalParticipants.query.filter(rentalid=rentalid).all()
    
    if len(rentalpeople) >= minpeople:
        rental.status = Confirmed
    else :
        retal_status = Pending
    db.session.commit()

    return jsonify({'success': 'successfully update rental status'})

# userid 를 통해 해당 유저의 usertype 반환
def methods_get_Users_usertype(userid) :
    user = Users.query.filter(Users.userid == userid).first()
    
    if not user:
        return jsonify({'error': 'invalid userid'})
    
    return jsonify({'usertype': user.usertype})

# dayofweek 을 받아서 Enum 값(정기 일정 요일)로 반환
def methods_convert_dayofweek(dayofweek) :
    
    if dayofweek = "Monday" :
        val = 0
    elif dayofweek = "Tuesday" :
        val = 1
    elif dayofweek = "Wednesday" :
        val = 2
    elif dayofweek = "Thursday" :
        val = 3
    elif dayofweek = "Friday" :
        val = 4
    elif dayofweek = "Saturday" :
        val = 5
    else :
        val = 6
    return jsonify({'dayofweek':val})

# 일정의 인원수 를 받아서 Enum 값(일정 상태)로 반환
def methods_convert_status(max_p, cur_p, min_p) :
    
    if cur_p < min_p :
        return jsonify({'status': "Pending"})  
    elif min_p <= cur_p and cur_p < max_p :
        return jsonify({'status': "Confirmed"})
    elif cur_p == max_p :
        return jsonify({'status': "Restricted"})

    return jsonify({'dayofweek':val})

