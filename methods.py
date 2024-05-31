from db import *
from methods import *
from flask import *
from datetime import *
from flask_jwt_extended import *


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
            rental.rentalflag = Rentals_Flags_enum.Fix
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
                rental.rentalflag = Rentals_Flags_enum.Fix

    db.session.commit()

# 초기 데이터 설정
#def methods_init_datas() :
    # Sportspaces (0,1,2)

