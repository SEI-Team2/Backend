from db import *
from methods import *
from flask import *
from datetime import *
from flask_jwt_extended import *

notifications_bp = Blueprint('notifications', __name__)


# 유저 공지 조회
@notifications_bp.route('/list', methods=['POST'])
@jwt_required()
def notifications_list():
    current_userid = get_jwt_identity()
    notifications = db.session.query(Notifications).filter(Notifications.userid == current_userid)
    
    notifications_data = []
    for notification in notifications :
        
        notificationid = notification.notificationid
        notifytype = notification.notifytype.name
        msg = ""
        timestmap_str = notification.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        status = notification.status.name
        
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
    
        if notifytype == 'rental_fix' or notifytype == 'rental_cancle' :
            sportsspace = db.session.query(SportsSpace).filter(SportsSpace.spaceid == spaceid).first()
            if not sportsspace :
                continue
            spacename = sportsspace.name
            starttime_str = notification.starttime.strftime('%Y-%m-%d %H:%M:%S')
            endtime_str = notification.endtime.strftime('%Y-%m-%d %H:%M:%S')

        elif notifytype == 'friend_request' or notifytype == 'friend_accept' or notifytype == 'friend_reject' :
            friend = db.session.query(Users).filter(Users.userid == friendid).first()
            if not friend :
                continue
            friendstudentid = friend.studentid
            friendname = friend.name
            friendcontact = friend.contact
            friendemail = friend.email
         
        elif notifytype == 'club_member_add' or notifytype == 'club_member_delete' or notifytype == 'club_manager_add' or notifytype == 'club_manager_delete' :
            club = db.session.query(Clubs).filter(Clubs.clubid == clubid).first()
            if not club :
                continue
            clubname = club.name
    

        notifications_data.append({
            'notificationid' : notificationid,
            'notifytype' : notifytype,
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
            
    return jsonify({'notifications' : notifications_data}), 200

# 유저 공지 읽음 처리
@notifications_bp.route('/read', methods=['POST'])
@jwt_required()
def notifications_read():
    current_userid = get_jwt_identity()
    data = request.json
    notificationid = data.get('notificationid')
    
    if not notificationid :
        return jsonify({'error': 'Notification ID are required'}), 400
    
    notification = db.session.query(Notifications).filter(Notifications.notificationid == notificationid, Notifications.userid == current_userid).first()
    
    if not notification :
        return jsonify({'error': 'Notification is not exist'}), 401
    
    notification.status = Notifications_ReadStatus_enum.Read
    db.session.commit()
    
    return jsonify({'message': 'Notification read successfully'}), 200


    