from db import *
from methods import *
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required, get_jwt_identity

rentals_bp = Blueprint('rentals', __name__)

# 대여 조회(참여 가능한 일정들만)
@rentals_bp.route('/list', methods=['GET'])
@jwt_required()
def rentals_list():
    methods_update_rentals()
    current_userid = get_jwt_identity()
    data = request.json

    spaceid = data.get('spaceid')
    date_str = data.get('date')

    if not spaceid or not date_str:
        return jsonify({'error': 'Space ID and date are required'}), 400

    if not (0 <= spaceid or spaceid <= 2) :
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
        Rentals.rentalstatus != Rentals_Status_enum.Close,
        _or(Rentals.status == Rentals_Status_enum.Light,
        Rentals.status == Rentals_Status_enum.Club)
    ).all()

    rentals_list = []
    for rental in rentals :
        rentals_List.append({
            'rentalid': rental.rentalid,
            'spaceid': rental.spaceid,
            'userid': rental.userid,

            'clubid': rental.clubid,
            'timelimit': rental.timelimit,
            
            'starttime': rental.starttime.strftime('%Y-%m-%d %H:%M:%S'),
            'endtime': rental.endtime.strftime('%Y-%m-%d %H:%M:%S'),
            'createtime': rental.createtime.strftime('%Y-%m-%d %H:%M:%S'),
            
            'maxpeople': rental.maxpeople,
            'minpeople': rental.minpeople,
            'people': rental.people,

            'rentaltype': rental.rentaltype.name,
            'rentalstatus': rental.rentalstatus.name,
            'rentalsflag': rental.rentalsflag.name,

            'desc' : rental.desc, 
        })

    return jsonify({'rentals' : rentals_list}), 200


# 대여 참여
@rentals_bp.route('/join', methods=['GET'])
@jwt_required()
def rentals_join():
    methods_update_rentals()
    current_userid = get_jwt_identity()
    data = request.json

    rentalid = data.get('rentalid')

    if not rentalid :
        return jsonify({'error': 'Rental ID are required'}), 400

    rental = db.session.query(Rentals).filter(
        Rentals.rentalid == rentalid,
        Rentals.status != Rentals_Status_enum.Close,
    ).first()

    if not rental :
        return jsonify({'error': 'Rental ID is invalid'}), 400

    # Light 일정에 참여하는 경우
    if rental.rentaltype == Rentals_Types_enum.Light :
        rentalparticipant = db.session.query(RentalParticipants).filter(RentalParticipants.rentalid == rentalid, participantid == current_userid).first()
    
        if rentalparticipant : 
            return jsonify({'error': 'You already participated in'}), 400

        rentalparticipant = RentalParticipants(rentalid = rentalid, participantid = current_userid)
        db.session.add(rentalparticipant)
        rental.poeple += 1

    # Club 일정에 참여하는 경우
    elif rental.rentaltype == Rentals_Types_enum.Club :
        rentalparticipant = db.session.query(RentalParticipants).filter(RentalParticipants.rentalid == rentalid, participantid == current_userid).first()
    
        if rentalparticipant : 
            return jsonify({'error': 'You already participated in'}), 400

        # 동아리 인원만 모집중인 경우
        if rental.rentalstatus == Rentals_Status_enum.Half :
            clubmember = db.session.query(ClubMembers).filter(ClubMembers.userid == current_userid, ClubMembers.clubid == rental.clubid).first()
            # 동아리 회원인 경우
            if clubmember : 
                rentalparticipant = RentalParticipants(rentalid = rentalid, participantid = current_userid)
                db.session.add(rentalparticipant)
                rental.poeple += 1
            
            # 동아리 회원 아닌 경우
            else :
                return jsonify({'error': 'You cannot join the Club'}), 400
        # 동아리 인원 모집 후 추가 모집
        elif rental.rentalstatus == Rentals_Status_enum.Open :
            rentalparticipant = RentalParticipants(rentalid = rentalid, participantid = current_userid)
            db.session.add(rentalparticipant)
            rental.poeple += 1

    db.session.commit()

    return jsonify({}), 200


# Light 대여 생성
@rentals_bp.route('/create', methods=['GET'])
@jwt_required()
def rentals_create():
    methods_update_rentals()
    current_userid = get_jwt_identity()
    data = request.json

    spaceid = data.get('spaceid')
    starttime_str = data.get('starttime')
    starttime = datetime.strptime(starttime_str, '%Y-%m-%d %H:%M:%S')
    endtime_str = data.get('endtime')
    endtime = datetime.strptime(endtime_str, '%Y-%m-%d %H:%M:%S')
    maxpeople = data.get('maxpeople')
    desc = data.get('desc')
    friends = data.get('friends',[])

    # spaceid 검사
    if not (0 <= sapceid <= 2) :
        return jsonify({'error': 'Invalid spaceid'}), 400
    
    # time 검사
    if startime >= endtime :
        return jsonify({'error': 'Invalid starttime and endtime'}), 400

    if not (6 <= starttime.hour <= 22) or not (6 <= endtime.hour <= 22) :
        return jsonify({'error': 'Invalid starttime and endtime'}), 400

    rental = db.session.query(Rentals).filter(
        Rentals.spaceid == spaceid,
        Rentals.starttime >= starttime,
        Rentals.endtime <= endtime,
    ).first()
    if rental :
        return jsonify({'error': 'Rental already exist'}), 400
    
    # maxpeople 검사
    sportspace = db.session.query(SportSpace).filter(
        SportSpace.spaceid == spaceid
    ).first() 
    if not (sportspace.minpeople <= maxpeople <= sportspace.maxpeople) :
        return jsonify({'error': 'Invalid maxpeople value'}), 400

    # friends 검사 및 초대 알림 생성
    for friend in friends :
        user = db.session.query(Users).filter(Users.studentid == friend).first() 
        if not user :
            continue
        friendid = user.userid
        notification = Notifications(userid = friendid, msg = "Invited to schedule", timestamp = datetime.utcnow(), status = Notifications_ReadStatus_enum.Unread, rentalid = rental.rentalid)
        db.session.add(notification)

    # rental 생성
    rental = Rentals(spaceid = spaceid, userid = current_userid, starttime = starttime, endtime = endtime, createtime = datetime.utcnow(), maxpeople = maxpeople, minpeolple = sportspace.minpeople, people = 1, rentaltype = Rentals_Types_enum.Light, rentalstatus = Rentals_Status_enum.Open, rentalsflag = Rentals_Flags_enum.Nonfix, desc = desc)
    db.session.add(rental)

    # user 를 일정에 추가
    rentalparticipant = RentalParticipants(rentalid = rental.rentalid, participantid = current_userid)
    db.session.add(rentalparticipant)
    
    db.session.commit()
    return jsonify({}), 200