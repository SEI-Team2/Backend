from db import *
from methods import *
from flask import *
from datetime import *
from flask_jwt_extended import *


# 렌탈에 대한 인원 변동시, 해당 렌탈의 status 를 갱신
def methods_update_Users_status(rentalid) :
    rental = Rentals.query.filter(Rentals.rentalid == rentalid).first()
    if not rental:
        return jsonify({'error': 'invalid rentalid'})

    spaceid = rental.spaceid

    sportspace = SportsSpace.query.filter(SportsSpace.spaceid == spaceid).first()
    if not sportspace:
        return jsonify({'error': 'invalid space id'})

    minpeople = sportspace.minpeople

    rentalpeople = RentalParticipants.query.filter(rentalid=rentalid).all()
    
    if len(rentalpeople) >= minpeople:
        rental.status = Confirmed
    else :
        retal_status = Pending
    db.session.commit()

    return jsonify({'success': 'successfully update rental status'})

# userid 를 통해 해당 유저의 usertype 반환
def methods_get_Users_usertype(userid) :
    user = Users.query.filter(Users.userid == userid).first()
    
    if not user:
        return jsonify({'error': 'invalid userid'})
    
    return jsonify({'usertype': user.usertype})

# 일정의 인원수 를 받아서 Enum 값(일정 상태)로 반환
def methods_convert_status(max_p, cur_p, min_p) :
    if cur_p < min_p :
        return jsonify({'status': "Pending"})  
    elif min_p <= cur_p and cur_p < max_p :
        return jsonify({'status': "Confirmed"})
    elif cur_p == max_p :
        return jsonify({'status': "Restricted"})

    return jsonify({'dayofweek':val})

# spacetype Enum 을 종목 명으로 반환
def methods_convert_spacetype(spacetype) :
    if spacetype == 0 :
        return "테니스"
    elif spacetype == 1 :
        return "농구"
    else :
        return "축구"

# Rentals 의 모든 튜플들 갱신
def methods_update_rentals( ) :

    rentals = db.session.query(Rentals).all()

    for rental in rentals : 
        
        ## 모든 일정에 대해 ##
        # 지난 일정은 삭제
        if datetime.utcnow() >= rental.starttime :
            db.session.delete(rental)
            continue

        ## 동아리 대여 일정인 경우 
        if rental.rentaltype == Rentals_Types_enum.Club :
            # 인원이 다 찼으면, Close
            if rental.people >= rental.maxpeople :
                rental.rentalstatus = Rentals_Status_enum.Close
                continue

            # 아직 timelimit 전인 경우, Half
            if datetime.utcnow() <= rental.starttime - timedelta(hour=rental.timelimit) :
                rental.rentalstatus = Rentals_Status_enum.Half         
            # timelimit 지난 경우, Open
            else :
                rental.rentalstatus = Rentals_Status_enum.Open
            continue

        ## 관리자제한 일정인 경우 
        elif rental.status == Rentals_Status_enum.Restrict :
            rental.rentalstatus = Rentals_Status_enum.Close
            rental.rentalsflag = Rentals_Flags_enum.Fix
            continue
        
        ## 일반 대여 일정인 경우 ##
        else :
            # 인원에 따른 status, Open | Close
            if rental.people >= rental.maxpeople :
                rental.rentalstatus = Rentals_Status_enum.Close
            else :
                rental.rentalstatus = Rentals_Status_enum.Open
            
            # 인원에 따른 flags, Fix | Nonfix
            if rental.people >= rental.minpeople :
                rental.rentalsflag = Rentals_Flags_enum.Fix

    db.session.commit()

# 초기 데이터 설정
#def methods_init_datas() :
    # Sportspaces (0,1,2)

