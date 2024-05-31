from db import *
from methods import *
from flask import *
from datetime import *
from flask_jwt_extended import *

notifications_bp = Blueprint('notifications', __name__)


# 유저 공지 조회
# TODO for frontend :
# 1. jwt
# 2. status = 0 : 읽지 않은 상태.
@notifications_bp.route('/list', methods=['GET'])
@jwt_required()
def notifications_list():
    current_userid = get_jwt_identity()
    notifications = db.session.query(Notifications).filter(Notifications.userid == current_userid)

    notifications_data = []
    for notification in notificaions :
        
        notificationid = notification.notificationid
        notifytype = notification.notifytype
        msg = ""
        timestmap_str = notification.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        status = notification.status
        
        rentalid = notification.rentalid
        spaceid = notification.spaceid
        spacename = None
        starttime_str = None
        endtime_str = None
                
        friendid = notification.friendid
        friendstudentid = None
        friendname = None
        friendcontact = None
        friendemail = None

        clubid = notification.clubid
        clubname = None

        match notification.notifytype :
            case 0 | 1 :
                sportsspace = db.session.query(SportsSpace).filter(SportsSpace.spaceid == spaceid).first()
                if not sportsspace :
                    continue
                spacename = sportsspace.name
                starttime_str = notification.starttime.strftime('%Y-%m-%d %H:%M:%S')
                endtime_str = notification.endtime.strftime('%Y-%m-%d %H:%M:%S')
                break
            case 2 | 3 | 4 :
                friend = db.session.query(Users).filter(Users.userid == friendid).first()
                if not friend :
                    continue
                friendstudentid = friend.studentid
                friendname = friend.name
                friendcontact = friend.contact
                friendemail = friend.email
                break
            case 5 | 6 | 7 | 8 :
                club = db.session.query(Clubs).filter(Clubs.clubid == clubid).first()
                if not club :
                    continue
                clubname = club.name
                break
            case _ :
                break

        notification_list.append({
            'notificationid' : notificationid,
            'notifytype' : notifytype.name,
            'msg': msg,
            'timestamp': timestmap_str,
            'status': status,

            'rentalid' : rentalid,
            'spaceid' : spaceid,
            'spacename' : spacename,
            'starttime' : starttime_str,
            'endtime' : endtime_str,
            
            'friendid' : friendid,
            'friendstudentid' : friendstudentid,
            'friendname' : friendname,
            'friendcontact' : friendcontact,
            'friendemail' : friendemail,

            'clubid' : clubid,
            'clubname' : clubname,
        })
            
    return jsonify({'notifications' : notification_data}), 200



    