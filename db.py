from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from enums import *
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'Users'
    userid = db.Column(db.Integer, primary_key=True)
    studentid = db.Column(db.String(255), unique=True, nullable=False) # 학번
    name = db.Column(db.String(255), nullable=False) # 이름
    contact = db.Column(db.String(255), unique=True, nullable=False) # 전화번호
    email = db.Column(db.String(255), unique=True, nullable=False) # 이메일
    verified = db.Column(db.Boolean, default = False)
    usertype = db.Column(EnumType(Users_UserType_enum), default = Student) # 권한
    regtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # 가입 시각
    password_hash = db.Column(db.String(100), nullable=False) # 패스워드
    
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Friends(db.Model):
    __tablename__ = 'Friends'
    userid1 = db.Column(db.Integer, primary_key=True, ForeignKey('Users.userid')) # 발신자
    userid2 = db.Column(db.Integer, primary_key=True, ForeignKey('Users.userid')) # 수신자
    status = db.Column(EnumType(Friends_Status_enum), nullable=False, default=Friends_Status_enum.Pending)

class SportsSpace(db.Model):
    __tablename__ = 'Sportsspace'
    spaceid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False) 
    location = db.Column(db.String(255))
    createtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    spacetype = db.Column(EnumType(SportSpaces_Type_enum), nullable=True)
    minpeople = db.Column(db.Integer, nullable=False)
    maxpeople = db.Column(db.Integer, nullable=False)
    timelimit = db.Column(db.Integer, nullable=False)
    courtnumber = db.Column(db.Integer, nullable=False)

class Rentals(db.Model):
    __tablename__ = 'Rentals'
    rentalid = db.Column(db.Integer, primary_key=True)
    spaceid = db.Column(db.Integer, nullable=False)  
    userid = db.Column(db.Integer, nullable=False) 
    clubid = db.Column(db.Integer, default = None)
    starttime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    endtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  
    createtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status =  db.Column(EnumType(Rentals_Status_enum), nullable=False, default = Rentals_Status_enum.Pending)
    maxpeople = db.Column(db.Integer, nullable=False)
    people = db.Column(db.Integer, nullable=False)
    minpeople = db.Column(db.Integer, nullable=False)
    # 동아리 정기 일정에 대한 핸들링

class RentalParticipants(db.Model):
    __tablename__ = 'Rentalparticipants'
    rentalid = db.Column(db.Integer, primary_key=True) 
    participantid = db.Column(db.Integer, primary_key=True, ForeignKey('Users.userid')) 

class LightningRentals(db.Model):
    __tablename__ = 'Lightningrentals'
    slotid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, primary_key=True)

class Clubs(db.Model):
    __tablename__ = 'Clubs'
    clubid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique = True, nullable=False)
    createtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class ClubMembers(db.Model):
    __tablename__ = 'Clubmembers'
    userid = db.Column(db.Integer, primary_key=True, ForeignKey('Users.userid'))
    clubid = db.Column(db.Integer, primary_key=True, ForeignKey('Clubs.clubid'))
    role = db.Column(db.EnumType(Clubmembers_Role_enum), default=Member)

class ClubRentals(db.Model):
    __tablename__ = 'Clubrentals'
    clubrentalid = db.Column(db.Integer, primary_key=True)
    clubid = db.Column(db.Integer, nullable=False)
    spaceid = db.Column(db.Integer, nullable=False)
    dayofweek = db.Column(EnumType(ClubRentals_Dayofweek_enum), nullable=False) 
    starttime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    endtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  
    createtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Notifications(db.Model):
    __tablename__ = 'Notifications'
    notificationid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer,ForeignKey('Users.userid').nullable = False)   
    msg = db.Column(db.Text, nullable = False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(EnumType(Notifications_ReadStatus_enum), nullable=False, default = Unread)

class Blacklist(db.Model):
    __tablename__ = 'Blacklist'
    blackid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, ForeignKey('Users.userid'), ondelete='CASCADE')
    reason = db.Column(db.Text, primary_key=True) 
    createtime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

