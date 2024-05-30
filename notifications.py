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
    notifications = Notifications.query.filter_by(Notifications.userid==current_userid,Notifications.readstatus==Notifications_ReadStatus_enum.Unread).all()

    notifications_list = []
    for notification in notificaions :
            notification_list.append({
                'notificationid' : notificaions.notificationid,
                'msg': notification.msg,
                'timestamp': notification.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'status': notification.status,
                'rentalid' : notification.rentalid,
                'friendid' : notification.friendid,
                'clubid' : notification.clubid,
            })
            
    return jsonify({'notifications' : notification_list}), 200

# 공지사항을 열람 후, {rentalid, friendid, clubid} 타입에 따라, 해당 탭으로 리다이렉션 수행
