from db import *
from methods import *
from flask import *
from datetime import *
from flask_jwt_extended import *

clubs_bp = Blueprint('clubs', __name__)

# 동아리 목록 조회
# TODO for frontend :
# 1. jwt 토큰 
# 2. 등록된 모든 동아리와 각 동아리 목록 반환
@clubs_bp.route('/clubs', methods=['GET'])
@jwt_required()
def clubs_clubs():
    current_userid = get_jwt_identity()
    data = request.json

    clubs =  db.session.query(Clubs).all()

    if not clubs :
        return jsonify({"error" : "Clubs not exist" }), 400

    clubs_data = []
    for club in clubs :
        clubs_data.append({
            'clubid' : club.clubid,
            'name' : club.name,
        })

    return jsonify(clubs_data), 200



# 동아리 관리자 명단 조회
# TODO for frontend :
# 1. jwt 토큰 
# 2. 등록된 모든 동아리와 각 동아리의 매니저 목록 반환
@clubs_bp.route('/clubmanagers', methods=['GET'])
@jwt_required()
def clubs_clubmanagers():
    current_userid = get_jwt_identity()
    data = request.json

    clubmanagers = db.session.query(ClubMembers).filter_by(role == Clubmembers_Role_enum.Manager).all()
    if not clubmanagers :
        return jsonify({"error" : "Clubmanagers not exist" }), 400

    clubmanagers_data = []
    for clubmanager in clubmanagers :
        user = Users.query.filter_by(Users.userid == clubmanager.userid).first()
        club = db.session.query(Clubs).filter_by(clubid == clubmanager.clubid).first()
        if not user or not club :
            continue
        clubmanagers_data.append({
            'clubname' : club.name,
            'userid' : user.userid,
            'studentid' : user.studentid,
            'name' : user.name,
            'contact': user.contact,
            'email' : user.email,
        })
    return jsonify(clubmanagers_data), 200

# 동아리 관리자 삭제
@clubs_bp.route('/clubmanager/delete', methods=['GET'])
@jwt_required()
def clubs_clubmanager_delete():
    current_userid = get_jwt_identity()
    data = request.json

    studentid = data.get('studentid')

    # user 탐색
    user = db.session.query(Users).filter_by(Users.studentid == studentid).first()
    if not user:
        return jsonify({"error" : "Studentid not exist" }), 400
    if user.usertype != Users_UserType_enum.Clubmanager :
        return jsonify({"error" : "Not manager of club" }), 400

    # ClubMembers 탐색
    clubmember = db.session.query(Clubmembers).filter_by(userid == user.userid, roll == Users_UserType_enum.Clubmanager).first()
    if not clubmember :
        return jsonify({"error" : "clubmember not exist" }), 400
    clubid = clubmember.clubid
    db.session.delete(clubmember) 

    # 튜플 갱신
    user.usertype = Users_UserType_enum.Student
    db.session.add(Clubmembers(userid = user.userid, clubid = clubid, roll = Clubmembers_Role_enum.Member))
    db.session.commit()

    return jsonify({}), 200


# 동아리 관리자 추가
@clubs_bp.route('/clubmanager/add', methods=['GET'])
@jwt_required()
def clubs_clubmanager_register():
    current_userid = get_jwt_identity()
    data = request.json

    clubid = data.get('clubid')
    studentid = data.get('studentid')

    # club 탐색
    club = db.session.query(Clubs).filter_by(Clubs.clubid == clubid).first()
    if not club :
        return jsonify({"error" : "Club not exist" }), 400

    # user 탐색
    user = db.session.query(Users).filter_by(Users.studentid == studentid).first()
    if not user:
        return jsonify({"error" : "Studentid not exist" }), 400
    if user.usertype == Users_UserType_enum.Clubmanager :
        return jsonify({"error" : "Already manager of club" }), 400

    # ClubMembers 탐색
    clubmember = db.session.query(Clubmembers).filter_by(userid == user.userid, clubid == club.clubid).first()
    if clubmember :
        db.session.delete(clubmemeber)
    
    # 튜플 갱신
    user.usertype = Users_UserType_enum.Clubmanager
    db.session.add(Clubmembers(userid = user.userid, clubid = club.clubid, roll = Clubmembers_Role_enum.Manager))
    db.session.commit()

    return jsonify({}), 200


# 동아리 정기 일정 목록
@clubs_bp.route('/clubregular', methods=['GET'])
@jwt_required()
def clubs_clubregular():
    current_userid = get_jwt_identity()
    data = request.json
    
    clubregulars = db.session.query(ClubRegulars).all()
    
    clubregulars_data = []
    for clubregular in clubregulars :
        rental = db.session.query(Rentals).query(Rentals.clubregularid == clubregular.clubregularid).first()
        if not rental :
            db.session.delete(clubregular)
            continue
        club = db.session.query(Clubs).query(Clubs.clubid == clubregular.clubid).first()
        if not club :
            db.session.delete(clubregular)
            continue
        clubregulars_data.append({
            'clubregularid' : clubregular.clubregularid,
            'clubid' : clubregular.clubid,
            'clubname' : club.name,
            'spaceid' : clubregular.spaceid,
            'dayofweek' : clubregular.dayofweek,
            'starttime' : clubregular.starttime,
            'endtime' : clubregular.endtime,
        })

    return jsonify({'clubregulars' : clubregulars_data}), 200


# 동아리 정기 일정 추가
@clubs_bp.route('/clubregular/add', methods=['GET'])
@jwt_required()
def clubs_clubregular_add():
    current_userid = get_jwt_identity()
    data = request.json

    clubid = data.get('clubid')
    spaceid = data.get('spaceid')
    dayofweek = data.get('dayofweek') # M=0, T=1, W=2, ...  S=6
    starttime_str = data.get('starttime')
    endtime_str = data.get('endtime')
    nums = data.get('nums')

    try:
        starttime = datetime.strptime(starttime_str, '%H:%M:%S').time()
        endtime = datetime.strptime(endtime_str, '%H:%M:%S').time()
    except ValueError:
        return jsonify({'error': 'Invalid time format, expected HH:MM:SS'}), 400
    if not(0 <= spaceid <=2) :
        return jsonify({'error': 'Invalid day of the week'}), 400
    if not (0 <= weekofday <= 6):
        return jsonify({'error': 'Invalid day of the week'}), 400
    if not nums :
        return jsonify({'error': 'nums must be given'}), 400


    clubregular = ClubRegulars(clubid = clubid, spaceid = spaceid, dayofweek = dayofweek, starttime = starttime, endtime = endtime)
    db.session.add(clubregular)

    sportsspace = db.session.query(SportsSpace).filter(SportsSpace.spaceid == spaceid).first()

    # 다가올 X요일 탐색
    today = datetime.today()
    days_ahead = weekofday - today.weekday()
    if days_ahead < 0:
        days_ahead += 7
    next_occurrence = today + timedelta(days=days_ahead)

    for i in range(nums):
        start_datetime = datetime.combine(next_occurrence, starttime)
        end_datetime = datetime.combine(next_occurrence, endtime)

        # 현재 시간 이후인지 확인
        if datetime.utcnow() >= start_datetime :
            next_occurrence += timedelta(days=7)
            continue

        # 기존 일정이 있는지 확인
        rental = db.session.query(Rentals).filter(
            Rentals.spaceid == spaceid,
            _or((Rentals.starttime >= start_datetime,
            Rentals.starttime <= end_datetime),
            (Rentals.endtime >= start_datetime,
            Rentals.endtime <= end_datetime))
        ).first()
        if rentals :
            continue

        new_rental = Rentals(
            spaceid=spaceid,  
            userid=current_userid,

            clubid=clubid,
            clubregularid = clubregular.clubregularid,
            timelimit = 72,

            starttime=start_datetime,
            endtime=end_datetime,
    
            maxpeople= sportsspace.maxpeople , 
            minpeople= sportsspace.minpeople,
            people=0,  

            rentaltype=Rentals_Types_enum.Club,
            rentalstatus=Rentals_Status_enum.Open,
            rentalflag=Rentals_Flags_enum.Fix,  
            
        )
        
        db.session.add(new_rental)
        next_occurrence += timedelta(days=7) 

    db.session.commit()

    return jsonify({}), 200


# 동아리 정기 일정 삭제
@clubs_bp.route('/clubregular/delete', methods=['GET'])
@jwt_required()
def clubs_clubregular_delete():
    current_userid = get_jwt_identity()
    data = request.json

    clubregularid = data.get('clubregularid')

    clubregular =  db.session.query(ClubRegulars).filter(ClubRegulars.clubregularid == clubregularid).first()
    if not clubregular :
        return jsonify({"error" : "clubregular not exist" }), 400

    rentals = db.session.query(Rentals).filter(Rentals.rentaltype == Rentals_Types_enum.Club, Rentals.clubregularid == clubregularid)
    for rental in rentals :
        # 렌탈 참여자 삭제
        rentalparticipants = db.session.query(RentalParticipants).filter(RentalParticipants.rentalid == rental.rentalid).all()
        for rentalparticipant in rentalparticipants :
            db.session.delete(rentalparticipant)    
        # 렌탈 삭제
        db.session.delete(rental)
    
    # 정기일정 삭제
    db.session.delete(clubregular)

    db.session.commit()

    return jsonify({}), 200


