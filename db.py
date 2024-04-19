from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from enums import *
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Users(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    studentid = db.Column(db.String(255), unique=True, nullable=False) # 학번
    name = db.Column(db.String(255), nullable=False) # 이름
    contract = db.Column(db.String(255), unique=True, nullable=False) # 전화번호
    email = db.Column(db.String(255), unique=True, nullable=False) # 이메일
    password_hash = db.Column(db.String(100), nullable=False) # 패스워드
    usertype = db.Column(EnumType(Users_UserType_enum), nullable=False) # 0 = 일반학생, 1 = 동아리회장, 2 = 조교

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class SportsSpace(db.Model):
    spaceid = db.Column(db.Integer, primary_key=True) 
    minpeople = db.Column(db.Integer, nullable=False)
    timelimit = db.Column(db.Integer, nullable=False)
    courtnumber = db.Column(db.Integer, nullable=False)
    
class ClubTimeSlotParticipants(db.Model):
    slotid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, primary_key=True)

class Friends(db.Model):
    userid1 = db.Column(db.Integer, primary_key=True)
    userid2 = db.Column(db.Integer, primary_key=True) 
    status = db.Column(EnumType(Friends_Status_enum), nullable=False, default=Friends_Status_enum.Pending)

class Rentals(db.Model):
    rentalid = db.Column(db.Integer, primary_key=True)
    spaceid = db.Column(db.Integer, nullable=False)  
    userid = db.Column(db.Integer, nullable=False) 
    starttime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    endtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  
    createtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status =  db.Column(EnumType(Rentals_Status_enum), nullable=False, default = Rentals_Status_enum.Pending)
    minpeoplemet =  db.Column(db.Boolean, nullable=False)

class Notifications(db.Model):
    notificationid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer,nullable = False)   
    msg = db.Column(db.Text, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    readstatus = db.Column(EnumType(Notifications_ReadStatus_enum), nullable=False, default = Notifications_ReadStatus_enum.Unread)

class Clubs(db.Model):
    clubid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    chairid = db.Column(db.Integer, nullable=False)

class RentalParticipants(db.Model):
    rid = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)
    status = db.Column(EnumType(RentalParticipants_Status_enum),nullable=False,default=RentalParticipants_Status_enum.Invited)

class Clubmembers(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    clubid = db.Column(db.Integer, primary_key=True) 

class ClubTimeSlots(db.Model):
    slotid = db.Column(db.Integer, primary_key=True)
    spaceid = db.Column(db.Integer, nullable=False)
    clubid =   db.Column(db.Integer, nullable=False)
    starttime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    endtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(EnumType(ClubTimeSlots_Status_enum), nullable=False, default=ClubTimeSlots_Status_enum.Pending)
    minpeoplemet =  db.Column(db.Boolean, nullable=False)
