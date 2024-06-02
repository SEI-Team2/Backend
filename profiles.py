from db import *
from methods import *
from flask import *
from datetime import *
from flask_jwt_extended import *

profiles_bp = Blueprint("profiles", __name__)


# 유저 정보
@profiles_bp.route("/user", methods=["GET"])
@jwt_required()
def profiles_user():
    current_userid = get_jwt_identity()

    user = db.session.query(Users).filter(Users.userid == current_userid).first()

    if not user:
        return jsonify({"error": "User not found"}), 400

    # 유저 정보 반환
    return (
        jsonify(
            {
                "name": user.name,
                "contact": user.contact,
                "email": user.email,
                "studentid": user.studentid,
                "usertype": Users_UserType_enum(user.usertype).name,
            }
        ),
        200,
    )


# 학번으로 유저 정보 조회
@profiles_bp.route("/user/<studentid>", methods=["GET"])
@jwt_required()
def profiles_user_studentid(studentid):
    current_userid = get_jwt_identity()

    user = db.session.query(Users).filter(Users.studentid == studentid).first()

    if not user:
        return jsonify({"error": "User not found"}), 400

    # 유저 정보 반환
    return (
        jsonify(
            {
                "name": user.name,
                "contact": user.contact,
                "email": user.email,
                "studentid": user.studentid,
                "usertype": Users_UserType_enum(user.usertype).name,
            }
        ),
        200,
    )


# 유저 참여 일정 조회
@profiles_bp.route("/schedules", methods=["GET"])
@jwt_required()
def profiles_schedules():
    methods_update_rentals()
    current_userid = get_jwt_identity()

    rentalparticipants = (
        db.session.query(RentalParticipants)
        .filter(RentalParticipants.participantid == current_userid)
        .all()
    )
    if not rentalparticipants:
        return jsonify({"error": "No rental schedules"}), 400

    schedules = []
    for rentalparticipant in rentalparticipants:
        rental = (
            db.session.query(Rentals)
            .filter(Rentals.rentalid == rentalparticipant.rentalid)
            .first()
        )
        if not rental:
            continue
        # rental.userid로부터 user 정보 가져오기
        user = db.session.query(Users).filter(Users.userid == rental.userid).first()
        
        schedules.append(
            {
                "rentalid": rental.rentalid,
                "spaceid": rental.spaceid,
                "userid": rental.userid,
                "rental owner name": user.name,
                "rental owner phone": user.contact,
                "clubid": rental.clubid,
                "timelimit": rental.timelimit,
                "starttime": rental.starttime.strftime("%Y-%m-%d %H:%M:%S"),
                "endtime": rental.endtime.strftime("%Y-%m-%d %H:%M:%S"),
                "createtime": rental.createtime.strftime("%Y-%m-%d %H:%M:%S"),
                "maxpeople": rental.maxpeople,
                "minpeople": rental.minpeople,
                "people": rental.people,
                "rentaltype": Rentals_Types_enum(rental.rentaltype).name,
                "rentalstatus": Rentals_Status_enum(rental.rentalstatus).name,
                "rentalflag": Rentals_Flags_enum(rental.rentalflag).name,
                "desc": rental.desc,
            }
        )

    return jsonify({"schedules": schedules}), 200


# 본인 동아리원 목록 조회
@profiles_bp.route("/clubmembers/list", methods=["GET"])
@jwt_required()
def profiles_clubmembers_list():
    current_userid = get_jwt_identity()

    # 어느 동아리 회장인지 탐색
    clubmanager = (
        db.session.query(ClubMembers)
        .filter(
            ClubMembers.userid == current_userid,
            ClubMembers.role == Clubmembers_Role_enum.Manager,
        )
        .first()
    )
    if not clubmanager:
        return jsonify({"error": "clubmanager not exist"}), 400

    # 동아리 탐색
    club = db.session.query(Clubs).filter(Clubs.clubid == clubmanager.clubid).first()
    if not club:
        return jsonify({"error": "Mananging club not exist"}), 401

    # 동아리 회원 탐색
    clubmembers = (
        db.session.query(ClubMembers)
        .filter(
            ClubMembers.clubid == club.clubid,
            ClubMembers.role == Clubmembers_Role_enum.Member,
        )
        .all()
    )

    clubmembers_data = []
    for clubmember in clubmembers:
        user = db.session.query(Users).filter(Users.userid == clubmember.userid).first()
        clubmembers_data.append(
            {
                "userid": user.userid,
                "studentid": user.studentid,
                "name": user.name,
                "contact": user.contact,
                "email": user.email,
            }
        )
    return jsonify({"clubmembers": clubmembers_data}), 200

# 특정 동아리원 목록 조회(동아리 이름 활용)
@profiles_bp.route("/clubmembers/list/<clubname>", methods=["GET"])
@jwt_required()
def profiles_clubmembers_list_clubname(clubname):
    current_userid = get_jwt_identity()

    # 동아리 탐색
    club = db.session.query(Clubs).filter(Clubs.name == clubname).first()
    if not club:
        return jsonify({"error": "Club not exist"}), 400

    # 동아리 회원 탐색
    clubmembers = (
        db.session.query(ClubMembers)
        .filter(
            ClubMembers.clubid == club.clubid,
            ClubMembers.role == Clubmembers_Role_enum.Member,
        )
        .all()
    )

    clubmembers_data = []
    for clubmember in clubmembers:
        user = db.session.query(Users).filter(Users.userid == clubmember.userid).first()
        clubmembers_data.append(
            {
                "userid": user.userid,
                "studentid": user.studentid,
                "name": user.name,
                "contact": user.contact,
                "email": user.email,
            }
        )
    return jsonify({"clubmembers": clubmembers_data}), 200

# 동아리원 목록 추가
@profiles_bp.route("/clubmembers/add", methods=["POST"])
@jwt_required()
def profiles_clubmembers_add():
    current_userid = get_jwt_identity()
    data = request.json

    studentid = data.get("studentid")

    # 어느 동아리 회장인지 탐색
    clubmanager = (
        db.session.query(ClubMembers)
        .filter(
            ClubMembers.userid == current_userid,
            ClubMembers.role == Clubmembers_Role_enum.Manager,
        )
        .first()
    )
    if not clubmanager:
        return jsonify({"error": "clubmanager not exist"}), 400

    # 동아리 탐색
    club = db.session.query(Clubs).filter(Clubs.clubid == clubmanager.clubid).first()
    if not club:
        return jsonify({"error": "Mananging club not exist"}), 401

    # 추가할 유저 탐색
    user = Users.query.filter(Users.studentid == studentid).first()
    if not user:
        return jsonify({"error": "User not exist"}), 402

    # 유저가 이미 동아리에 있는지 확인
    clubmember = (
        db.session.query(ClubMembers).filter(ClubMembers.userid == user.userid).first()
    )
    if clubmember:
        return jsonify({"error": "User exist in clubmember"}), 403

    # 유저를 동아리 회원으로 추가
    db.session.add(
        ClubMembers(
            userid=user.userid, clubid=club.clubid, role=Clubmembers_Role_enum.Member
        )
    )
    db.session.commit()

    # 알림 #
    notify = Notifications(
        userid=user.userid,
        notifytype=Notifications_Types_enum.club_member_add,
        clubid=club.clubid,
    )
    db.session.add(notify)
    db.session.commit()
    # 알림 #

    db.session.commit()

    return jsonify({}), 200

# 동아리원 목록 추가(동아리 이름, 유저 이름, 학번 활용)
@profiles_bp.route("/clubmembers/add/<clubname>", methods=["POST"])
@jwt_required()
def profiles_clubmembers_add_clubname(clubname):
    current_userid = get_jwt_identity()
    data = request.json

    studentid = data.get("studentid")

    # 동아리 탐색
    club = db.session.query(Clubs).filter(Clubs.name == clubname).first()
    if not club:
        return jsonify({"error": "Club not exist"}), 400

    # 추가할 유저 탐색
    user = Users.query.filter(Users.studentid == studentid).first()
    if not user:
        return jsonify({"error": "User not exist"}), 401

    # 유저가 이미 동아리에 있는지 확인
    clubmember = (
        db.session.query(ClubMembers)
        .filter(
            ClubMembers.userid == user.userid,
            ClubMembers.clubid == club.clubid,
            ClubMembers.role == Clubmembers_Role_enum.Member,
        )
        .first()
    )
    if clubmember:
        return jsonify({"error": "User exist in clubmember"}), 402

    # 유저를 동아리 회원으로 추가
    db.session.add(
        ClubMembers(
            userid=user.userid, clubid=club.clubid, role=Clubmembers_Role_enum.Member
        )
    )
    db.session.commit()

    # 알림 #
    notify = Notifications(
        userid=user.userid,
        notifytype=Notifications_Types_enum.club_member_add,
        clubid=club.clubid,
    )
    db.session.add(notify)
    db.session.commit()
    # 알림 #

    db.session.commit()

    return jsonify({}), 200

# 동아리원 목록 삭제
# TODO for frontend :
# 1. [jwt 토큰 + 유저이름 + 유저학번]
# 2. 현재 유저가 동아리 담당자 자격임을 가정합니다.
@profiles_bp.route("/clubmembers/delete", methods=["POST"])
@jwt_required()
def profiles_clubmembers_delete():
    current_userid = get_jwt_identity()
    data = request.json

    studentid = data.get("studentid")

    # 어느 동아리 회장인지 탐색
    clubmanager = (
        db.session.query(ClubMembers)
        .filter(
            ClubMembers.userid == current_userid,
            ClubMembers.role == Clubmembers_Role_enum.Manager,
        )
        .first()
    )
    if not clubmanager:
        return jsonify({"error": "clubmanager not exist"}), 401

    # 동아리 탐색
    club = db.session.query(Clubs).filter(Clubs.clubid == clubmanager.clubid).first()
    if not club:
        return jsonify({"error": "Mananging club not exist"}), 402

    # 삭제할 유저 탐색
    user = Users.query.filter(Users.studentid == studentid).first()
    if not user:
        return jsonify({"error": "User not exist"}), 403

    # 유저가 이미 동아리에 있는지 확인
    clubmember = (
        db.session.query(ClubMembers)
        .filter(
            ClubMembers.userid == user.userid,
            ClubMembers.clubid == club.clubid,
            ClubMembers.role == Clubmembers_Role_enum.Member,
        )
        .first()
    )
    if not clubmember:
        return jsonify({"error": "User not exist in clubmember or manager"}), 404

    # 유저를 동아리 회원에서 삭제
    db.session.delete(clubmember)
    db.session.commit()

    # 알림 #
    notify = Notifications(
        userid=user.userid,
        notifytype=Notifications_Types_enum.club_member_delete,
        clubid=club.clubid,
    )
    db.session.add(notify)
    db.session.commit()
    # 알림 #

    db.session.commit()

    return jsonify({}), 200

# 동아리원 목록 삭제(동아리 이름, 유저 이름, 학번 활용)
@profiles_bp.route("/clubmembers/delete/<clubname>", methods=["POST"])
@jwt_required()
def profiles_clubmembers_delete_clubname(clubname):
    current_userid = get_jwt_identity()
    data = request.json

    studentid = data.get("studentid")

    # 동아리 탐색
    club = db.session.query(Clubs).filter(Clubs.name == clubname).first()
    if not club:
        return jsonify({"error": "Club not exist"}), 400

    # 삭제할 유저 탐색
    user = Users.query.filter(Users.studentid == studentid).first()
    if not user:
        return jsonify({"error": "User not exist"}), 401

    # 유저가 이미 동아리에 있는지 확인
    clubmember = (
        db.session.query(ClubMembers)
        .filter(
            ClubMembers.userid == user.userid,
            ClubMembers.clubid == club.clubid,
            ClubMembers.role == Clubmembers_Role_enum.Member,
        )
        .first()
    )
    if not clubmember:
        return jsonify({"error": "User not exist in clubmember or manager"}), 402

    # 유저를 동아리 회원에서 삭제
    db.session.delete(clubmember)
    db.session.commit()

    # 알림 #
    notify = Notifications(
        userid=user.userid,
        notifytype=Notifications_Types_enum.club_member_delete,
        clubid=club.clubid,
    )
    db.session.add(notify)
    db.session.commit()
    # 알림 #

    db.session.commit()

    return jsonify({}), 200

# 회원 패스워드 변경
@profiles_bp.route("/settings/changepw", methods=["POST"])
@jwt_required()
def profiles_settings_changepw():
    current_userid = get_jwt_identity()
    data = request.json

    pw = data.get("pw")
    user = db.session.query(Users).filter(Users.userid == current_userid).first()

    if not user:
        return jsonify({"error": "User not found"}), 401

    user.set_password(pw)
    db.session.commit()

    return jsonify({}), 200

# 현재 User가 관리하는 모든 동아리 list 가져오는 API
@profiles_bp.route("/clubs", methods=["GET"])
@jwt_required()
def profiles_clubs():
    current_userid = get_jwt_identity()
    # 현재 User가 관리하는 모든 동아리 list 가져오기
    clubmanagers = (
        db.session.query(ClubMembers)
        .filter(
            ClubMembers.userid == current_userid,
            ClubMembers.role == Clubmembers_Role_enum.Manager,
        )
        .all()
    )

    if not clubmanagers:
        return jsonify({"error": "No club found"}), 400

    clubs = []
    for clubmanager in clubmanagers:
        club = db.session.query(Clubs).filter(Clubs.clubid == clubmanager.clubid).first()
        clubs.append(
            {
                "clubid": club.clubid,
                "name": club.name,
                "createtime": club.createtime.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    return jsonify({"clubs": clubs}), 200

# 