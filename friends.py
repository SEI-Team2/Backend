from db import *
from methods import *
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required, get_jwt_identity

friends_bp = Blueprint('friends', __name__)

# 받은 친구 요청 목록 
@friends_bp.route('/reqeusts/pending', methods=['GET'])
def friedns_requests_pending():
    data = request.json
    
    # TODO : Frineds 에서 해당 유저의 Pending 중인 요청들을 반환


# 보낸 친구 요청 목록 
@friends_bp.route('/reqeusts/sending', methods=['GET'])
def friends_requests_sending():
    data = request.json

    # TODO : Friends 에서 해당 유저가 Sending 중인 요청들을 반환


# 친구 목록 
@friends_bp.route('/list', methods=['GET'])
def friends_list():
    data = request.json
    
    # TODO : Friends 에서 해당 유저와 친구인 유저의 Profile을 반환




