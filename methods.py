from db import *
from methods import *
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required, get_jwt_identity

# 렌탈에 대한 인원 변동시, 해당 렌탈의 status 를 갱신
def methods_update_Users_status(rentalid):
    
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
def methods_get_Users_usertype(userid):
    user = Users.query.filter(Users.userid == userid).first()
    
    if not user:
        return jsonify({'error': 'invalid userid'})
    
    return jsonify({'usertype': user.usertype})