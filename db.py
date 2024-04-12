from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from enums import *
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Users(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String(25), unique=True, nullable=False) # 학번
    name = db.Column(db.String(25), nullable=False) # 이름
    phone = db.Column(db.String(25), unique=True, nullable=False) # 전화번호
    email = db.Column(db.String(50), unique=True, nullable=False) # 이메일
    password_hash = db.Column(db.String(100), nullable=False) # 패스워드
    usertype = db.Column(EnumType(Users_UserType_enum), nullable=False) # 0 = 일반학생, 1 = 동아리회장, 2 = 조교
    
    def __repr__(self):
        return '<User %r>' % self.name

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Clubs(db.Model):
    cid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    chair = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Club %r>' % self.name


class Rentals(db.Model):
    rid = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.Integer, nullable=False)  
    uid = db.Column(db.Integer, nullable=False) 
    stime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) #
    etime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # 
    status =  db.Column(EnumType(Rentals_Status_enum), nullable=False, default = Rentals_Status_enum.Pending)
    minpeoplemet =  db.Column(db.Boolean, nullable=False)
    def __repr__(self):
        return '<User %r>' % self.sid


class RentalParticipants(db.Model):
    rid = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)
    status = db.Column(EnumType(RentalParticipants_Status_enum),nullable=False,default=RentalParticipants_Status_enum.Invited)
    def __repr__(self):
        return '<User %r>' % self.rid


class Clubmembers(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer, nullable=False) 
    def __repr__(self):
        return '<User %r>' % self.uid


class Friends(db.Model):
    uid1 = db.Column(db.Integer, primary_key=True)
    uid2 = db.Column(db.Integer, nullable=False) # 학번
    status = db.Column(EnumType(Friends_Status_enum), nullable=False, default=Friends_Status_enum.Pending)
    def __repr__(self):
        return '<User %r>' % self.uid1


class SportsSpace(db.Model):
    sid = db.Column(db.Integer, primary_key=True)
    stype = db.Column(EnumType(SportSpaces_Type_enum), nullable=False, default=SportSpaces_Type_enum.Tennis) 
    minpeople = db.Column(db.Integer, nullable=False)
    courtnumber = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<User %r>' % self.sid


class ClubTimeSlots(db.Model):
    sid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(EnumType(SportSpaces_Type_enum), nullable=False, default=SportSpaces_Type_enum.Tennis) 
    dayofweek = db.Column(EnumType(ClubTimeSlots_DayOfWeek_enum), nullable=False)
    stime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    etime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(EnumType(ClubTimeSlots_Status_enum), nullable=False, default=ClubTimeSlots_Status_enum.Allocated)
    def __repr__(self):
        return '<User %r>' % self.sid
