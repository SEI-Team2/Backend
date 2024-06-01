from db import *
from methods import *
from flask import *
from datetime import *
from flask_jwt_extended import *

profiles_bp = Blueprint('profiles', __name__)

# 유저 정보
@profiles_bp.route('/user', methods=['POST'])
@jwt_required()
def profiles_user():
    current_userid = get_jwt_identity()
    data = request.json

    user = db.session.query(Users).filter(Users.userid == current_userid).first()

    if not user:
        return jsonify({'error': 'User not found'}), 400

    # 유저 정보 반환
    return jsonify({'name' : user.name, 'contact' : user.contact, 'email' : user.email, 'studentid' : user.studentid, 'usertype' : user.usertype.name}), 200


# 유저 참여 일정 조회
@profiles_bp.route('/schedules', methods=['POST'])
@jwt_required()
def profiles_schedules():
    methods_update_rentals()
    current_userid = get_jwt_identity()
    data = request.json

    rentalparticipants = db.session.query(RentalParticipants).filter(RentalParticipants.participantid == current_userid).all()
    if not rentalparticipants :
        return jsonify({'error': 'No rental schedules'}), 400

    schedules = []
    for rentalparticipant in rentalparticipants :
        rental = db.session.query(Rentals).filter(Rentals.rentalid == rentalparticipant.rentalid).first()        
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
            'rentalflag': rental.rentalflag.name,

            'desc' : rental.desc,
        })


    return jsonify({'schedules' : schedules}), 200


# 동아리원 목록 조회
@profiles_bp.route('/clubmembers/list', methods=['POST'])
@jwt_required()
def profiles_clubmembers_list():
    current_userid = get_jwt_identity()
    data = request.json
    
    # 어느 동아리 회장인지 탐색
    clubmanager = db.session.query(ClubMembers).filter(ClubMembers.userid == current_userid, ClubMembers.role == Clubmembers_Role_enum.Manager).first()     
    if not clubmanager :
        return jsonify({'error' : 'clubmanager not exist'}), 400

    # 동아리 탐색
    club = db.session.query(Clubs).filter(Clubs.clubid == clubmanager.clubid).first()     
    if not club :
        return jsonify({'error': 'Mananging club not exist'}), 401

    # 동아리 회원 탐색
    clubmembers = db.session.query(ClubMembers).filter(ClubMembers.clubid == club.clubid, ClubMembers.role == Clubmembers_Role_enum.Member).all()  

    clubmembers_data = []
    for clubmember in clubmembers :
        user = db.session.query(Users).filter(Users.userid == clubmember.userid).first()
        clubmembers_data.append({
            'userid' : user.userid,
            'studentid' : user.studentid,
            'name' : user.name,
            'contact' : user.contact,
            'email' : user.email,
        })
    return jsonify({'clubmembers' : clubmembers_data}), 200


# 동아리원 목록 추가
@profiles_bp.route('/clubmembers/add', methods=['POST'])
@jwt_required()
def profiles_clubmembers_add():
    current_userid = get_jwt_identity()
    data = request.json

    studentid = data.get('studentid')

    # 어느 동아리 회장인지 탐색
    clubmanager = db.session.query(ClubMembers).filter(ClubMembers.userid == current_userid, ClubMembers.role == Clubmembers_Role_enum.Manager).first()     
    if not clubmanager :
        return jsonify({'error' : 'clubmanager not exist'}), 400

    # 동아리 탐색
    club = db.session.query(Clubs).filter(Clubs.clubid == clubmanager.clubid).first()     
    if not club :
        return jsonify({'error': 'Mananging club not exist'}), 401

    # 추가할 유저 탐색
    user = Users.query.filter(Users.studentid == studentid).first()
    if not user :
        return jsonify({'error': 'User not exist'}), 402

    # 유저가 이미 동아리에 있는지 확인
    clubmember = db.session.query(ClubMembers).filter(ClubMembers.userid == user.userid).first()
    if clubmember :
        return jsonify({'error': 'User exist in clubmember'}), 403
    
    # 유저를 동아리 회원으로 추가
    db.session.add(ClubMembers(userid = user.userid, clubid = club.clubid, role = Clubmembers_Role_enum.Member))
    db.session.commit()

    # 알림 #
    notify = Notifications(userid = user.userid, notifytype=Notifications_Types_enum.club_member_add, clubid=club.clubid)
    db.session.add(notify)
    db.session.commit()
    # 알림 #

    db.session.commit()

    return jsonify({}), 200


# 동아리원 목록 삭제
# TODO for frontend :
# 1. [jwt 토큰 + 유저이름 + 유저학번]
# 2. 현재 유저가 동아리 담당자 자격임을 가정합니다.
@profiles_bp.route('/clubmembers/delete', methods=['POST'])
@jwt_required()
def profiles_clubmembers_delete():
    current_userid = get_jwt_identity()
    datas = request.json

    studentid = data.get('studentid')

    # 어느 동아리 회장인지 탐색
    clubmanager = db.session.query(ClubMembers).filter(ClubMembers.userid == current_userid, ClubMembers.role == Clubmembers_Role_enum.Manager).first()     
    if not clubmanager :
        return jsonify({'error' : 'clubmanager not exist'}), 401

    # 동아리 탐색
    club = db.session.query(Clubs).filter(Clubs.clubid == clubmanager.clubid).first()     
    if not club :
        return jsonify({'error': 'Mananging club not exist'}), 402

    # 삭제할 유저 탐색
    user = Users.query.filter(Users.studentid == studentid).first()
    if not user :
        return jsonify({'error': 'User not exist'}), 403

    # 유저가 이미 동아리에 있는지 확인
    clubmember = db.session.query(ClubMembers).filter(ClubMembers.userid == user.userid, ClubMembers.clubid == club.clubid, ClubMembers.roll == Clubmembers_Role_enum.Member).first()
    if not clubmember :
        return jsonify({'error': 'User not exist in clubmember or manager'}), 404
    
    # 유저를 동아리 회원에서 삭제
    db.session.delete(clubmember)
    db.session.commit()

    # 알림 #
    notify = Notifications(userid = user.userid, notifytype=Notifications_Types_enum.club_member_delete, clubid=club.clubid)
    db.session.add(notify)
    db.session.commit()
    # 알림 #

    db.session.commit()

    return jsonify({}), 200




# 회원 패스워드 변경
@profiles_bp.route('/settings/changepw', methods=['POST'])
@jwt_required()
def profiles_settings_changepw():
    current_userid = get_jwt_identity()
    data = request.json

    pw = data.get('pw')
    user = db.session.query(Users).filter(Users.userid == current_userid).first()
    
    if not user:
        return jsonify({'error': 'User not found'}), 401

    user.set_password(pw)
    db.session.commit()
    
    return jsonify({}), 200
   
    