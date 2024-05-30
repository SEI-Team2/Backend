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
@profiles_bp.route('/user', methods=['GET'])
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
@profiles_bp.route('/schedules', methods=['GET'])
@jwt_required()
def profiles_schedules():
    methods_update_rentals()
    current_userid = get_jwt_identity()
    data = request.json

    rentalparticipants = db.session.query(RentalParticipants).filter_by(participantid == current_userid).all()
    if not rentalparticipants :
        return jsonify({'error': 'No rental schedules'}), 400

    schedules = []
    for rentalparticipant in rentalparticipants :
        rental = db.session.query(Rentals).filter_by(rentalid == rentalparticipant.rentalid).first()        
        if not rental :
            continue
        schedules.append({
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


    return jsonify({rental_data}), 200


# 동아리원 목록 조회
# TODO for frontend :
# 1. jwt 토큰
# 2. 현재 유저가 동아리 담당자 자격임을 가정합니다.
# 3. [{name,studentid,contact,email}]
@profiles_bp.route('/clubmemebers/list', methods=['GET'])
@jwt_required()
def profiles_clubmembers_list():
    current_userid = get_jwt_identity()
    data = request.json
    
    # 동아리 쿼리
    clubmember = db.session.query(ClubMembers).filter_by(userid == current_userid, role == Clubmembers_Role_enum.Manager).first()     
    club = db.session.query(Clubs).filter_by(clubid == clubmember.clubid).first()     

    # 동아리 회원 쿼리
    members = db.session.query(ClubMembers).filter_by(clubid == club.clubid, role == Clubmembers_Role_enum.Member).all()  

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
@profiles_bp.route('/clubmemebers/add', methods=['GET'])
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

    # 알림 생성 : 동아리 가입 회원에게 알림
    notification = Notifications(userid = user.userid, msg = "동아리에 가입되었습니다!", timestamp = datetime.utcnow ,status = Notifications_ReadStatus_enum.Unread, clubid = club.clubid)
    db.session.add(clubmember)
    # 알림 생성

    db.session.commit()
    return jsonify({}), 200


# 동아리원 목록 삭제
# TODO for frontend :
# 1. [jwt 토큰 + 유저이름 + 유저학번]
# 2. 현재 유저가 동아리 담당자 자격임을 가정합니다.
@profiles_bp.route('/clubmemebers/delete', methods=['POST'])
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


# 회원 패스워드 변경
# TODO for frontend :
# 1. jwt 토큰 + 변경할 패스워드
# 2. 패스워드 변경 결과를 반환합니다.
@profiles_bp.route('/settings/changepw', methods=['GET'])
@jwt_required()
def profiles_settings_changepw():
    current_userid = get_jwt_identity()
    data = request.json

    pw = data.get('pw')
    user = db.session.query(Users).filter_by(userid == current_userid).first()
    
    if not user:
        return jsonify({'error': 'User not found'}), 400

    user.set_password(pw)
    db.session.commit()
    return jsonify({}), 200
   
    