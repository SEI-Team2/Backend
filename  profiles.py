from db import *
from methods import *
from flask import *
from datetime import *
from flask_jwt_extended import *

profiles_bp = Blueprint('profiles', __name__)

# 유저 정보
# TODO for frontend :
# 1. jwt 토큰
# 2. 현재 유저 정보{name,contact,email,studentid}를 반환합니다.
@users_bp.route('/user', methods=['GET'])
@jwt_required()
def profiles_user():
    current_userid = get_jwt_identity()
    user = db.session.query(Users).filter_by(userid == current_userid).first()
    
    if not user:
        return jsonify({'error': 'User not found'}), 400

    # 유저 정보 반환
    return jsonify({'name' : user.name, 'contact' : user.contact, 'email' : user.email, 'studentid' : user.studentid}), 200


# 유저 참여 일정 조회
# TODO for frontend :
# 1. jwt 토큰
# 2. 현재유저 참여중인 모든 일정들의 정보[{sport,starttime,endtime,people,clubname,status}]를 반환합니다.
# 3. clubname 이 있으면 동아리 일정, 없으면 일반 일정입니다.
@users_bp.route('/schedule', methods=['GET'])
@jwt_required()
def profiles_schedule():
    current_userid = get_jwt_identity()
    data = request.json

    rentalparticipants = db.session.query(RentalParticipants).filter_by(participantid == current_userid).all()
    if not rentalparticipants :
        return jsonify({'error': 'No rental schedules'}), 400

    rental_ids = set()
    for rentalparticipant in rentalparticipants :
        rental_ids.add(rentalparticipant.rentalid)

    rental_data = []
    for rental_id in rental_ids :
        rental = db.session.query(Rentals).filter_by(rentalid == rental_id).first()
        space = db.session.query(SportsSpace).filter_by(spaceid == rental.spaceid).first()
        club = db.session.query(Clubs).filter_by(clubid == rental.clubid).first()
        if not space :
            continue
        sport = methods_convert_spacetype(space.spacetype)
        startime = rental.starttime.strftime('%Y-%m-%d %H:%M:%S')
        endtime =  rental.endtime.strftime('%Y-%m-%d %H:%M:%S')
        people = rental.people

        # 만약 동아리 일정이라면 유효한 clubname 도 반환합니다. 
        clubname = ""
        if club :
            clubname = club.name
        
        # 일정의 {대기,확정,취소,제한} 상태를 반환합니다.
        status = ""
        if rental.status == 0 :
            status = "Pending"
        elif rental.status == 1 :
            status = "Confirmed"
        elif rental.status == 1 :
            status = "Failed"
        else :
            status = "Restricted"

        rental_data.append({
            'sport' : sport,
            'starttime' : starttime,
            'endtime' : endtime,
            'people' : people,
            'clubname' : clubname,
            'status' : status
        })

    return jsonify({rental_data}), 200


# 동아리원 목록 조회
# TODO for frontend :
# 1. jwt 토큰
# 2. 현재 유저가 동아리 담당자 자격임을 가정합니다.
# 3. [{name,studentid,contact,email}]
@users_bp.route('/clubmemebers/list', methods=['GET'])
@jwt_required()
def profiles_clubmembers_list():
    current_userid = get_jwt_identity()
    data = request.json
    
    # 동아리 쿼리
    clubmember = db.session.query(ClubMembers).filter_by(userid == current_userid, role == Manager).first()     
    club = db.session.query(Clubs).filter_by(clubid == clubmember.clubid).first()     

    # 동아리 회원 쿼리
    members = db.session.query(ClubMembers).filter_by(clubid == club.clubid, role == Member).all()  

    members_data = []
    for member in members :
        user = db.session.query(Users).filter_by(userid == member.userid).first()
        members_data.append({
            'name' : user.name,
            'studentid' : user.studentid,
            'contact' : user.contact,
            'email' : user.email
        })
    return jsonify({members_data}), 200


# 동아리원 목록 추가
# TODO for frontend :
# 1. jwt 토큰 + 유저이름 + 유저학번
# 2. 현재 유저가 동아리 담당자 자격임을 가정합니다.
@users_bp.route('/clubmemebers/add', methods=['GET'])
@jwt_required()
def profiles_clubmembers_add():
    current_userid = get_jwt_identity()
    data = request.json

    name = data.get('name')
    studentid = data.get('studentid')
    
    # 입력된 정보의 유저가 있는지 확인
    user = Users.query.filter_by(name == name, studentid == studentid).first()
    if not user :
        return jsonify({'error': 'User not exist'}), 400

    # 동아리 쿼리
    clubmember = db.session.query(ClubMembers).filter_by(userid == current_userid, role == Manager).first()     
    club = db.session.query(Clubs).filter_by(clubid == clubmember.clubid).first()  

    # 유저가 이미 동아리에 있는지 확인
    already = db.session.query(ClubMembers).filter_by(userid == user.userid, role == Member).first()
    if already :
        return jsonify({'error': 'User exist in clubmember'}), 400
    
    # 유저를 clubmember에 추가
    clubmember = ClubMembers(userid = user.userid,clubid = club.clubid, role = Member)
    db.session.add(clubmember)
    db.session.commit()
    return jsonify({}), 200


# 동아리원 목록 삭제
# TODO for frontend :
# 1. [jwt 토큰 + 유저이름 + 유저학번]
# 2. 현재 유저가 동아리 담당자 자격임을 가정합니다.
@users_bp.route('/clubmemebers/delete', methods=['POST'])
@jwt_required()
def profiles_clubmembers_delete():
    current_userid = get_jwt_identity()
    datas = request.json

    # 동아리 쿼리
    clubmember = db.session.query(ClubMembers).filter_by(userid == current_userid, role == Manager).first()     
    club = db.session.query(Clubs).filter_by(clubid == clubmember.clubid).first()  

    for data in datas :
        
        name = data.get('name')
        studentid = data.get('studentid')
        
        # 입력된 정보의 유저가 있는지 확인
        user = Users.query.filter_by(name == name, studentid == studentid).first()
        if not user :
            return jsonify({'error': 'User not exist'}), 400

        deletion_results = []

        rows_deleted = db.session.query(ClubMembers).filter_by(userid == user.userid, clubid == club.clubid, role == Member).delete()
        deletion_results.append((user.userid, club.clubid, rows_deleted))
        db.session.commit()
        for userid, clubid, rows_deleted in deletion_results:
            if rows_deleted > 0:
                return jsonify({}), 200 
            else:
                return jsonify({'error' : "User not exist as club member" }), 400



   
    