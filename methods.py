from db import *
from methods import *
from flask import *
from datetime import *
from flask_jwt_extended import *

# Rentals 의 모든 튜플들 갱신
def methods_update_rentals() :

    rentals = db.session.query(Rentals).all()

    for rental in rentals :   
        ## 모든 일정에 대해 ##
        # 지난 일정은 삭제
        if datetime.now() +  timedelta(hours=9) >= rental.endtime :
            db.session.delete(rental)
            db.session.commit()
            continue

        ## 동아리 대여 일정인 경우 
        if rental.rentaltype == Rentals_Types_enum.Club :
            # 72시간 넘게 남았을 때
            if datetime.now() + timedelta(hours=9) <= rental.starttime - timedelta(hours=72):
                if rental.people >= rental.maxpeople :
                    rental.rentalstatus = Rentals_Status_enum.Close
                    rental.rentalflag = Rentals_Flags_enum.Fix
                else:
                    rental.rentalstatus = Rentals_Status_enum.Half # 동아리원만 접근 가능
                    rental.rentalflag = Rentals_Flags_enum.Nonfix
            elif datetime.now() +  timedelta(hours=9) <= rental.starttime - timedelta(hours=1):
                if rental.people >= rental.maxpeople :
                    rental.rentalstatus = Rentals_Status_enum.Close
                    rental.rentalflag = Rentals_Flags_enum.Fix
                else:
                    rental.rentalstatus = Rentals_Status_enum.Open # 아무나 접근 가능
                    rental.rentalflag = Rentals_Flags_enum.Nonfix
            else:
                # 1시간도 안남았을 경우
                if rental.people >= rental.minpeople: # 최소인원 이상이면 확정
                    rental.rentalflag = Rentals_Flags_enum.Fix
                else: # 최소인원 미만이면 취소
                    rental.rentalflag = Rentals_Flags_enum.Nonfix
                    rental.rentalstatus = Rentals_Status_enum.Close
            db.session.commit()
            continue

        ## 관리자제한 일정인 경우 
        elif rental.rentaltype == Rentals_Types_enum.Restrict :
            rental.rentalstatus = Rentals_Status_enum.Close
            rental.rentalflag = Rentals_Flags_enum.Fix
            db.session.commit()
            continue
        
        ## 일반 대여 일정인 경우 ##
        else :
            if datetime.now() +  timedelta(hours=9) < rental.starttime - timedelta(hours=1):
                if rental.people >= rental.maxpeople : # 최대인원 이상이면 확정
                    rental.rentalstatus = Rentals_Status_enum.Close
                    rental.rentalflag = Rentals_Flags_enum.Fix
                else: # 최대인원 미만이면 모집중
                    rental.rentalstatus = Rentals_Status_enum.Open
                    rental.rentalflag = Rentals_Flags_enum.Nonfix
            else:
                if rental.people >= rental.minpeople : # 최소인원 이상이면 확정
                    rental.rentalflag = Rentals_Flags_enum.Fix 
                    rental.rentalstatus = Rentals_Status_enum.Close
                else: # 최소인원 미만이면 취소
                    rental.rentalflag = Rentals_Flags_enum.Nonfix
                    rental.rentalstatus = Rentals_Status_enum.Close
        db.session.commit()

    db.session.commit()

# 초기 데이터 설정
def methods_init_datas() :

    users = [
        Users(
            studentid="0000000000",
            name="admin",
            contact="01012341234",
            email="admin",
            usertype=Users_UserType_enum.Administrator,
        ),
        Users(
            studentid="23451",
            name="qan",
            contact="121212",
            email="email2",
            usertype=Users_UserType_enum.Student,
        ),
        Users(
            studentid="34512",
            name="wan",
            contact="131212",
            email="email3",
            usertype=Users_UserType_enum.Student,
        ),
        Users(
            studentid="45123",
            name="ean",
            contact="141212",
            email="email4",
            usertype=Users_UserType_enum.Clubmanager,
        ),
        Users(
            studentid="51234",
            name="ran",
            contact="151212",
            email="email5",
            usertype=Users_UserType_enum.Clubmanager,
        ),
        Users(
            studentid="2018311320",
            name="권우진",
            contact="01014351433",
            email="wojin57@g.skku.edu",
            usertype=Users_UserType_enum.Student,
        ),
        Users(
            studentid="2021317502",
            name="박성준",
            contact="0101241154",
            email="sj2park@g.skku.edu",
            usertype=Users_UserType_enum.Student,
        ),
    ]

    sportspaces = [
        SportsSpace(spaceid=0,name='TennisCourt', minpeople=8, maxpeople=16),
        SportsSpace(spaceid=1,name='BasketballCourt', minpeople=6, maxpeople=20),
        SportsSpace(spaceid=2,name='SoccerField', minpeople=10, maxpeople=22),
    ]

    clubs = [
        Clubs( name='트리플에스', createtime=datetime.now() +  timedelta(hours=9)),
        Clubs( name='STC', createtime=datetime.now() +  timedelta(hours=9)),
        Clubs( name='터보', createtime=datetime.now() +  timedelta(hours=9)),
        Clubs( name='애플트리', createtime=datetime.now() +  timedelta(hours=9)),
    ]

    clubmembers = [
        ClubMembers(userid =4, clubid=1, role = Clubmembers_Role_enum.Manager),
        ClubMembers(userid =5, clubid=2, role = Clubmembers_Role_enum.Manager)
        #ClubMembers(userid =3, clubid=3, role = Clubmembers_Role_enum.Member),
        #ClubMembers(userid =4, clubid=4, role = Clubmembers_Role_enum.Member).
    ]

    rentals = [
        #Rentals(spaceid=1, userid=1, starttime=datetime.now(), endtime=datetime.now()+timedelta(hours=1), maxpeople=10,minpeople=1,people=2,rentaltype=Rentals_Types_enum.Light,rentalstatus=Rentals_Status_enum.Open,rentalflag=Rentals_Flags_enum.Nonfix),
        #Rentals(spaceid=2, userid=1, clubid=1, starttime=datetime.now(), endtime=datetime.now()+timedelta(hours=1), maxpeople=10,minpeople=1,people=2,rentaltype=Rentals_Types_enum.Club,rentalstatus=Rentals_Status_enum.Close,rentalflag=Rentals_Flags_enum.Nonfix),
    ]

    check = db.session.query(Users).all()
    if not check :
        for user in users :
            user.set_password('password123')
            if user.name == 'admin':
                user.set_password('admin')
            if user.name == '권우진':
                user.set_password("Skkports")
            if user.name == '박성준':
                user.set_password("asdfgh")
            db.session.add(user)
            db.session.commit()    

    check = db.session.query(SportsSpace).all()
    if not check :
        db.session.add_all(sportspaces)
        db.session.commit()

    check = db.session.query(Clubs).all()
    if not check :
        db.session.add_all(clubs)
        db.session.commit()

    check = db.session.query(ClubMembers).all()
    if not check :
        db.session.add_all(clubmembers)
        db.session.commit()
