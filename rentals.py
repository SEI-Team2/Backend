from db import *
from methods import *
from flask import *
from datetime import *
from flask_jwt_extended import *
from sqlalchemy import *

rentals_bp = Blueprint('rentals', __name__)

@rentals_bp.route('/datetime', methods=['POST'])
@jwt_required()
def rentals_datetime():
    current_userid = get_jwt_identity()
    data = request.json
    date1 = datetime.now()
    date2 = datetime.now() +  timedelta(hours=9)
    return jsonify({'date1' : date1.strftime('%Y-%m-%d %H:%M:%S'), 'date2' : date2.strftime('%Y-%m-%d %H:%M:%S')}), 200


# 대여 조회(참여 가능한 일정들만)
@rentals_bp.route('/list', methods=['POST'])
@jwt_required()
def rentals_list():
    methods_update_rentals()
    current_userid = get_jwt_identity()
    data = request.json

    spaceid = data.get('spaceid')
    date_str = data.get('date')

    if not date_str:
        return jsonify({'error': 'Space ID and date are required'}), 400

    # if spaceid did not exist in the database, return error
    space = db.session.query(SportsSpace).filter(SportsSpace.spaceid == spaceid).first()
    if not space:
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
    or_(Rentals.rentaltype == Rentals_Types_enum.Light,
    Rentals.rentaltype == Rentals_Types_enum.Club)
    ).all()

    rentals_list = []
    for rental in rentals :
        name = "번개모임"
        if rental.rentaltype == Rentals_Types_enum.Club :
            club = db.session.query(Clubs).filter(Clubs.clubid == rental.clubid).first()
            if club :
                name = club.name
        rentals_list.append({
            'rentalid': rental.rentalid,
            'spaceid': rental.spaceid,
            'userid': rental.userid,

            'name' : name,
            
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
            'rentalflag': rental.rentalflag.name,

            'desc' : rental.desc, 
        })

    return jsonify({'rentals' : rentals_list}), 200


# 대여 참여
@rentals_bp.route('/join', methods=['POST'])
@jwt_required()
def rentals_join():
    methods_update_rentals()
    current_userid = get_jwt_identity()
    data = request.json

    rentalid = data.get('rentalid')

    if not rentalid :
        return jsonify({'error': 'Rental ID are required'}), 401

    rental = db.session.query(Rentals).filter(
    Rentals.rentalid == rentalid,
    Rentals.rentalstatus != Rentals_Status_enum.Close,
    ).first()

    if not rental :
        return jsonify({'error': 'Rental is not exist'}), 402

    # Light 일정에 참여하는 경우
    if rental.rentaltype == Rentals_Types_enum.Light :
        rentalparticipant = db.session.query(RentalParticipants).filter(RentalParticipants.rentalid == rentalid, RentalParticipants.participantid == current_userid).first()
    
        if rentalparticipant : 
            return jsonify({'error': 'You already participated in'}), 403

        rentalparticipant = RentalParticipants(rentalid = rentalid, participantid = current_userid)
        db.session.add(rentalparticipant)
        rental.people += 1

    # Club 일정에 참여하는 경우
    elif rental.rentaltype == Rentals_Types_enum.Club :
        rentalparticipant = db.session.query(RentalParticipants).filter(RentalParticipants.rentalid == rentalid, RentalParticipants.participantid == current_userid).first()
    
        if rentalparticipant : 
            return jsonify({'error': 'You already participated in'}), 404

        # 동아리 인원만 모집중인 경우
        if rental.rentalstatus == Rentals_Status_enum.Half :
            clubmember = db.session.query(ClubMembers).filter(ClubMembers.userid == current_userid, ClubMembers.clubid == rental.clubid).first()
            # 동아리 회원인 경우
            if clubmember : 
                rentalparticipant = RentalParticipants(rentalid = rentalid, participantid = current_userid)
                db.session.add(rentalparticipant)
                rental.people += 1
            
            # 동아리 회원 아닌 경우
            else :
                return jsonify({'error': 'You cannot join the Club'}), 405
        
        # 동아리 인원 모집 후 추가 모집
        elif rental.rentalstatus == Rentals_Status_enum.Open :
            rentalparticipant = RentalParticipants(rentalid = rentalid, participantid = current_userid)
            db.session.add(rentalparticipant)
            rental.people += 1

    db.session.commit()

    return jsonify({}), 200


# 대여 참여 취소
@rentals_bp.route('/cancle', methods=['POST'])
@jwt_required()
def rentals_cancle():
    methods_update_rentals()
    current_userid = get_jwt_identity()
    data = request.json

    rentalid = data.get('rentalid')

    rental = db.session.query(Rentals).filter(Rentals.rentalid == rentalid).first()
    if not rental :
        return jsonify({'error': 'rental not exist'}), 401
    if rental.rentalflag == Rentals_Flags_enum.Fix :
        return jsonify({'error': 'rental is fixed'}), 402
    if rental.userid == current_userid :
       return jsonify({'error': 'host cannot cancle'}), 404 
    rentalparticipant = db.session.query(RentalParticipants).filter(RentalParticipants.rentalid == rentalid, RentalParticipants.participantid == current_userid).first()
    if not rentalparticipant :
        return jsonify({'error': 'rentalparticipant not exist'}), 405
    db.session.delete(rentalparticipant)
    rental.people -= 1

    db.session.commit()

    return jsonify({}), 200


# Light 대여 생성
@rentals_bp.route('/create', methods=['POST'])
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
    maxpeople = int(data.get('maxpeople'))
    desc = data.get('desc')
    friends = data.get('friends',[])

    # spaceid 검사
    # if spaceid did not exist in the database, return error
    space = db.session.query(SportsSpace).filter(SportsSpace.spaceid == spaceid).first()
    if not space:
        return jsonify({'error': 'Space ID is invalid'}), 400

    # time 검사
    if starttime >= endtime :
        return jsonify({'error': 'Invalid starttime and endtime'}), 401

    if not (6 <= starttime.hour <= 22) or not (6 <= endtime.hour <= 22) :
        return jsonify({'error': 'Invalid starttime and endtime'}), 402

    rental = (
        db.session.query(Rentals)
        .filter(
            Rentals.spaceid == spaceid,
            or_(
                and_(Rentals.starttime <= starttime, starttime < Rentals.endtime),
                and_(Rentals.starttime < endtime, endtime <= Rentals.endtime),
                and_(starttime <= Rentals.starttime, Rentals.endtime <= endtime),
            ),
        )
        .first()
    )
    if rental :
        return jsonify({'error': 'Rental already exist'}), 403

    # maxpeople 검사
    sportsspace = db.session.query(SportsSpace).filter(
        SportsSpace.spaceid == spaceid
    ).first() 

    if not (sportsspace.minpeople <= maxpeople <= sportsspace.maxpeople) :
        return jsonify({'error': 'Invalid maxpeople value'}), 404

    # rental 생성
    rental = Rentals(spaceid = spaceid, userid = current_userid, starttime = starttime, endtime = endtime, createtime = datetime.now() + timedelta(hours=9), maxpeople = maxpeople, minpeople = sportsspace.minpeople, people = 0, rentaltype = Rentals_Types_enum.Light, rentalstatus = Rentals_Status_enum.Open, rentalflag = Rentals_Flags_enum.Nonfix, desc = desc)
    db.session.add(rental)
    db.session.commit()

    # user 를 일정에 추가
    rentalparticipant = RentalParticipants(rentalid = rental.rentalid, participantid = current_userid)
    db.session.add(rentalparticipant)
    db.session.commit()
    rental.people += 1

    # 친구들도 일정에 추가
    for friend in friends :
        user = db.session.query(Users).filter(Users.studentid == friend).first() 
        if not user :
            continue
        rentalparticipant = RentalParticipants(rentalid = rental.rentalid, participantid = user.userid)
        db.session.add(rentalparticipant)
        db.session.commit()
        rental.people += 1

    db.session.commit()

    return jsonify({}), 200


# 대여 삭제
@rentals_bp.route('/delete', methods=['POST'])
@jwt_required()
def rentals_delete():
    methods_update_rentals()
    current_userid = get_jwt_identity()
    data = request.json

    rentalid = data.get('rentalid')
    notify_users = []

    rental = db.session.query(Rentals).filter(Rentals.rentalid == rentalid, Rentals.userid == current_userid).first()
    if not rental :
        return jsonify({'error' : 'rental not exist'}), 400
    if rental.rentalflag == Rentals_Flags_enum.Fix :
        return jsonify({'error' : 'rental is fixed'}), 401    
    rentalparticipants = db.session.query(RentalParticipants).filter(RentalParticipants.rentalid == rentalid).all()
    for rentalparticipant in rentalparticipants :
        notify_users.append(rentalparticipant.participantid)
        db.session.delete(rentalparticipant)
        db.session.commit()
    
    # 알림 #
    for notify_user in notify_users :
        notify = Notifications(userid=notify_user, notifytype=Notifications_Types_enum.rental_cancle, spaceid=rental.spaceid, starttime=rental.starttime, endtime=rental.endtime)
        db.session.add(notify)
        db.session.commit()
    # 알림 #

    db.session.delete(rental)
    db.session.commit()

    return jsonify({}), 200
