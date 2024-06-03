from db import *
from methods import *
from flask import *
from datetime import *
from flask_jwt_extended import *

normals_bp = Blueprint('normals', __name__)

# 관리자제한 일정 추가
@normals_bp.route('/restrict', methods=['POST'])
@jwt_required()
def normals_restrict():
    methods_update_rentals()
    current_userid = get_jwt_identity()
    data = request.json

    spaceid = data.get('spaceid')

    starttime_str = data.get('starttime')
    starttime = datetime.strptime(starttime_str, '%Y-%m-%d %H:%M:%S')
    endtime_str = data.get('endtime')
    endtime = datetime.strptime(endtime_str, '%Y-%m-%d %H:%M:%S')

    rentaltype = Rentals_Types_enum.Restrict
    rentalstatus = Rentals_Status_enum.Close
    rentalflag = Rentals_Flags_enum.Fix

    desc = data.get('desc')

    rentals = (
        db.session.query(Rentals)
        .filter(
            Rentals.spaceid == spaceid,
            or_(
                and_(Rentals.starttime <= starttime, starttime < Rentals.endtime),
                and_(Rentals.starttime < endtime, endtime <= Rentals.endtime),
                and_(starttime <= Rentals.starttime, Rentals.endtime <= endtime),
            ),
        )
        .all()
    )

    # 일정 취소 및 취소 알림!!!!
    for rental in rentals :
        rentalparticipants = db.session.query(RentalParticipants).filter(RentalParticipants.rentalid == rental.rentalid).all()
        for rentalparticipant in rentalparticipants :
            # 알림 #
            db.session.add(
                Notifications(
                    userid=rentalparticipant.participantid,
                    timestamp=datetime.now(),
                    notifytype=Notifications_Types_enum.rental_cancle,
                    rentalid=rental.rentalid,
                    spaceid=rental.spaceid,
                    starttime=rental.starttime,
                    endtime=rental.endtime,
                )
            )
            db.session.commit()
            # 알림 #
            db.session.delete(rentalparticipant)
            db.session.commit()

        db.session.delete(rental)
        db.session.commit()

    # 관리자제한일정 추가
    restrict = Rentals(spaceid=spaceid, userid=current_userid, starttime=starttime, endtime=endtime, rentaltype=rentaltype, rentalstatus=rentalstatus, rentalflag=rentalflag, desc=desc)
    db.session.add(restrict)

    db.session.commit()

    return jsonify({}), 200


# 일반(Student, Clubmanager) | 블랙 명단 조회
@normals_bp.route('/black', methods=['GET'])
@jwt_required()
def normals_black():
    current_userid = get_jwt_identity()
    
    users = db.session.query(Users).filter(Users.usertype != Users_UserType_enum.Administrator).all()

    nonblack_data = []
    black_data = []
    for user in users :
        user_data = {
            'userid' : user.userid,
            'studentid' : user.studentid,
            'name' : user.name,
            'contact' : user.contact,
            'email' : user.email,
        }
        black = db.session.query(Blacklist).filter(Blacklist.userid == user.userid).first()
        if black :
            black_data.append(user_data)
        else :
            nonblack_data.append(user_data)
    return jsonify({'nonbalck' : nonblack_data, 'black' : black_data}), 200


# 블랙리스트 명단 추가
@normals_bp.route('/black/add', methods=['POST'])
@jwt_required()
def normals_black_add():
    current_userid = get_jwt_identity()
    data = request.json

    userid = data.get('userid')
    reason = data.get('reason')

    user = db.session.query(Users).filter(Users.userid == userid, Users.usertype != Users_UserType_enum.Administrator)
    if not user :
        return jsonify({'error' : 'User not exist'}), 401

    black = db.session.query(Blacklist).filter(Blacklist.userid == userid).first()
    if black :
        return jsonify({'error' : 'User already exist in blacklist'}), 402

    blacklist = Blacklist(userid=userid,reason=reason)
    db.session.add(blacklist)
    db.session.commit()
    
    return jsonify({}), 200


# 블랙리스트 명단 삭제
@normals_bp.route('/black/delete', methods=['POST'])
@jwt_required()
def normals_black_delete():
    current_userid = get_jwt_identity()
    data = request.json

    userid = data.get('userid')

    user = db.session.query(Users).filter(Users.userid == userid, Users.usertype != Users_UserType_enum.Administrator)
    if not user :
        return jsonify({'error' : 'User not exist'}), 401

    black = db.session.query(Blacklist).filter(Blacklist.userid == userid).first()
    if not black :
        return jsonify({'error' : 'User not exist in blacklist'}), 402

    db.session.delete(black)
    db.session.commit()
    
    return jsonify({}), 200
