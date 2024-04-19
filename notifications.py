from db import *
from methods import *
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required, get_jwt_identity

notifications_bp = Blueprint('notifications', __name__)

# 유저가 읽지 않은 공지 조회
@notifications_bp.route('/list', methods=['GET'])
@jwt_required()
def notifications_list():
    current_userid = get_jwt_identity()
    notifications = Notifications.query.filter_by(Notifications.userid==current_userid,Notifications.readstatus==Notifications_ReadStatus_enum.Unread).all()
    
    if not notifications:
        return jsonify({'error': 'No notifications found for this user'}), 404

    notifications_list = []

    for notification in notificaions :
            notification_data = {
                'notificationid' : notificaions.notificationid,
                'msg': notification.msg,
                'timestamp': notification.timestamp,
                'readstatus': notification.readstatus,
            }
            notifications_list.append(notification_data)
    return jsonify(notifications=notificaions_list), 200
