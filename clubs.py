from db import *
from methods import *
from flask import *
from datetime import *
from flask_jwt_extended import *

clubs_bp = Blueprint('clubs', __name__)

# 동아리 Club ID 조회 (동아리 이름 활용) GET API
@clubs_bp.route('/clubid/<clubname>', methods=['GET'])
@jwt_required()
def clubs_clubid(clubname):
    current_userid = get_jwt_identity()
    club = db.session.query(Clubs).filter(Clubs.name == clubname).first()
    if not club :
        return jsonify({"error" : "Club not exist" }), 400
    return jsonify({'clubid' : club.clubid}), 200


# 동아리 목록 조회
@clubs_bp.route('/clubs', methods=['POST'])
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
@clubs_bp.route('/clubmanagers', methods=['POST'])
@jwt_required()
def clubs_clubmanagers():
    current_userid = get_jwt_identity()
    data = request.json

    clubmanagers = db.session.query(ClubMembers).filter(ClubMembers.role == Clubmembers_Role_enum.Manager).all()
    if not clubmanagers :
        return jsonify({"error" : "Clubmanagers not exist" }), 401

    clubmanagers_data = []
    for clubmanager in clubmanagers :
        user = Users.query.filter(Users.userid == clubmanager.userid).first()
        club = db.session.query(Clubs).filter(Clubs.clubid == clubmanager.clubid).first()
        if not user or not club :
            continue
        clubmanagers_data.append({
            'clubid' : club.clubid,
            'clubname' : club.name,
            'userid' : user.userid,
            'studentid' : user.studentid,
            'name' : user.name,
            'contact': user.contact,
            'email' : user.email,
        })
    return jsonify(clubmanagers_data), 200

# 동아리 관리자 삭제
@clubs_bp.route('/clubmanagers/delete', methods=['POST'])
@jwt_required()
def clubs_clubmanagers_delete():
    current_userid = get_jwt_identity()
    data = request.json

    userid = data.get('userid')
    clubid = data.get('clubid')

    # user 탐색
    user = db.session.query(Users).filter(Users.userid == userid).first()
    if not user:
        return jsonify({"error" : "Userid not exist" }), 401
    if user.usertype != Users_UserType_enum.Clubmanager :
        return jsonify({"error" : "Not manager of club" }), 402

    # club 탐색
    club = db.session.query(Clubs).filter(Clubs.clubid == clubid).first()
    if not club :
        return jsonify({"error" : "club not exist" }), 403

    # ClubMembers 탐색
    clubmember = db.session.query(ClubMembers).filter(ClubMembers.userid == user.userid, ClubMembers.role == Clubmembers_Role_enum.Manager).first()
    if not clubmember :
        return jsonify({"error" : "clubmember not exist" }), 404
    db.session.delete(clubmember) 
    db.session.commit()

    # 튜플 갱신
    user.usertype = Users_UserType_enum.Student
    db.session.add(ClubMembers(userid = user.userid, clubid = club.clubid, role = Clubmembers_Role_enum.Member))
    db.session.commit()

    # 알림 #
    notify = Notifications( userid=user.userid, notifytype=Notifications_Types_enum.club_manager_delete, clubid=club.clubid)
    db.session.add(notify)
    db.session.commit()
    # 알림 #

    db.session.commit()

    return jsonify({}), 200

# 동아리 생성(동아리 스포츠 타입, 동아리 이름, 동아리 회장 학번)
@clubs_bp.route('/create', methods=['POST'])
@jwt_required()
def clubs_create():
    current_userid = get_jwt_identity()
    data = request.json

    clubid = data.get('clubid')
    name = data.get('name')
    presidentid = data.get('presidentid')

    # club 탐색
    club = db.session.query(Clubs).filter(Clubs.clubid == clubid).first()
    if club :
        return jsonify({"error" : "Club already exist" }), 400

    # user 탐색
    user = db.session.query(Users).filter(Users.studentid == presidentid).first()
    if not user:
        return jsonify({"error" : "Studentid not exist" }), 401
    if user.usertype != Users_UserType_enum.Student :
        return jsonify({"error" : "Not student" }), 402

    # 동아리 생성
    club = Clubs(clubid = clubid, name = name)
    db.session.add(club)
    db.session.commit()

    # 동아리 회장 추가
    db.session.add(ClubMembers(userid = user.userid, clubid = club.clubid, role = Clubmembers_Role_enum.Manager))
    db.session.commit()

    return jsonify({}), 200

# 동아리 관리자 추가
@clubs_bp.route('/clubmanagers/add', methods=['POST'])
@jwt_required()
def clubs_clubmanagers_add():
    current_userid = get_jwt_identity()
    data = request.json

    clubid = data.get('clubid')
    studentid = data.get('studentid')

    # club 탐색
    club = db.session.query(Clubs).filter(Clubs.clubid == clubid).first()
    if not club :
        # 없으면 동아리 생성
        club = Clubs(clubid = clubid, name = 'Club' + str(clubid))
        db.session.add(club)
        db.session.commit()
        
    # user 탐색
    user = db.session.query(Users).filter(Users.studentid == studentid).first()
    if not user:
        return jsonify({"error" : "Studentid not exist" }), 402
    if user.usertype == Users_UserType_enum.Clubmanager :
        return jsonify({"error" : "Already manager of club" }), 403

    # ClubMembers 탐색
    clubmembers = db.session.query(ClubMembers).filter(ClubMembers.userid == user.userid, ClubMembers.clubid == club.clubid).all()
    if clubmembers :
        for clubmember in clubmembers :
            db.session.delete(clubmember)
            db.session.commit()
    
    # 튜플 갱신
    user.usertype = Users_UserType_enum.Clubmanager
    db.session.add(ClubMembers(userid = user.userid, clubid = club.clubid, role = Clubmembers_Role_enum.Manager))
    db.session.commit()

    # 알림 #
    notify = Notifications(userid=user.userid, notifytype=Notifications_Types_enum.club_manager_add, clubid=club.clubid)
    db.session.add(notify)
    db.session.commit()
    # 알림 #
    
    db.session.commit()

    return jsonify({}), 200


# 동아리 정기 일정 목록
@clubs_bp.route('/clubregular', methods=['POST'])
@jwt_required()
def clubs_clubregular():
    current_userid = get_jwt_identity()
    data = request.json
    
    clubregulars = db.session.query(ClubRegulars).all()
    
    clubregulars_data = []
    for clubregular in clubregulars :
        rental = db.session.query(Rentals).filter(Rentals.clubregularid == clubregular.clubregularid).first()
        if not rental :
            db.session.delete(clubregular)
            db.session.commit()
            continue
        club = db.session.query(Clubs).filter(Clubs.clubid == clubregular.clubid).first()
        if not club :
            db.session.delete(clubregular)
            db.session.commit()
            continue
        clubregulars_data.append({
            'clubregularid' : clubregular.clubregularid,
            'clubid' : club.clubid,
            'clubname' : club.name,
            'spaceid' : club.spaceid,
            'dayofweek' : clubregular.dayofweek,
            'starttime' : clubregular.starttime.strftime('%H:%M:%S'),
            'endtime' : clubregular.endtime.strftime('%H:%M:%S'),
        })

    db.session.commit()

    return jsonify({'clubregulars' : clubregulars_data}), 200


# 동아리 정기 일정 추가
@clubs_bp.route('/clubregular/add', methods=['POST'])
@jwt_required()
def clubs_clubregular_add():
    methods_update_rentals()
    current_userid = get_jwt_identity()
    data = request.json

    clubid = data.get('clubid')
    spaceid = data.get('spaceid')
    dayofweek = data.get('dayofweek') # M=0, T=1, W=2, ...  S=6
    starttime_str = data.get('starttime')
    endtime_str = data.get('endtime')
    nums = data.get('nums')

    # 입력값 확인
    try:
        starttime = datetime.strptime(starttime_str, '%H:%M:%S').time()
        endtime = datetime.strptime(endtime_str, '%H:%M:%S').time()
    except ValueError:
        return jsonify({'error': 'Invalid time format, expected HH:MM:SS'}), 401
    
    if not (0 <= dayofweek <= 6):
        return jsonify({'error': 'Invalid dayofweek'}), 403
    if not nums :
        nums = 20
    # club id에 해당하는 동아리가 있는지 조회 -> 없음 생성
    club = db.session.query(Clubs).filter(Clubs.clubid == clubid).first()
    if not club :
        # 없으면 동아리 생성
        club = Clubs(clubid = clubid, name = 'Club' + str(clubid))
        db.session.add(club)
        db.session.commit()
    # 운동공간 탐색
    sportsspace = db.session.query(SportsSpace).filter(SportsSpace.spaceid == spaceid).first()
    if not sportsspace :
        return jsonify({'error': 'Invalid spaceid'}), 404
    
    # 클럽 정기일정 추가
    clubregular = ClubRegulars(clubid = clubid, spaceid = spaceid, dayofweek = dayofweek, starttime = starttime, endtime = endtime)
    db.session.add(clubregular)
    db.session.commit()
    # 다가올 X요일 탐색
    today = datetime.today()
    days_ahead = dayofweek - today.weekday()
    if days_ahead < 0:
        days_ahead += 7
    next_occurrence = today + timedelta(days=days_ahead)

    cnt = 0
    for i in range(nums):
        start_datetime = datetime.combine(next_occurrence, starttime)
        end_datetime = datetime.combine(next_occurrence, endtime)

        # 현재 시간 이후인지 확인
        if datetime.now() >= start_datetime :
            next_occurrence += timedelta(days=7)
            continue

        # 기존 일정이 있는지 확인
        rentals = db.session.query(Rentals).filter(
        Rentals.spaceid == spaceid,
        or_(
            and_(Rentals.starttime >= start_datetime, Rentals.starttime <= end_datetime),
            and_(Rentals.endtime >= start_datetime, Rentals.endtime <= end_datetime)
        )
        ).all()
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
            rentalstatus=Rentals_Status_enum.Half,
            rentalflag=Rentals_Flags_enum.Nonfix,  
            
        )
        
        cnt += 1
        db.session.add(new_rental)
        db.session.commit()
        next_occurrence += timedelta(days=7) 

    if cnt == 0 :
        db.session.delete(clubregular)
        db.session.commit()
        return jsonify({'error' : 'Cannot add clubregular'}), 405    
    db.session.commit()
    return jsonify({}), 200


# 동아리 정기 일정 삭제
@clubs_bp.route('/clubregular/delete', methods=['POST'])
@jwt_required()
def clubs_clubregular_delete():
    methods_update_rentals()
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
            # 알림 #
            notify = Notifications(userid=rentalparticipant.participantid, notifytype=Notifications_Types_enum.rental_cancle, rentalid=rental.rentalid, spaceid=rental.spaceid, starttime=rental.starttime, endtime=rental.endtime)
            db.session.add(notify)
            db.session.commit()
            # 알림 #
            db.session.delete(rentalparticipant)
            db.session.commit()
        # 렌탈 삭제
        db.session.delete(rental)
        db.session.commit()
    # 정기일정 삭제
    db.session.delete(clubregular)
    db.session.commit()

    return jsonify({}), 200


