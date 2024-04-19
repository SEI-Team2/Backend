from enum import Enum 
from sqlalchemy import Enum as EnumType

class Users_UserType_enum(Enum) : 
    Student = 0
    Chairperson = 1
    Administrator = 2

class Friends_Status_enum(Enum) : 
    Pending = 0
    Accepted = 1

class SportSpaces_Type_enum(Enum) : 
    TennisCourt = 0
    BasketballCourt = 1
    SoccerField = 2

class Rentals_Status_enum(Enum) : 
    Pending = 0
    Confirmed = 1
    Rejected = 2

class RentalParticipants_Status_enum(Enum) : 
    Invited = 0
    Accepted = 1

class ClubTimeSlots_Status_enum(Enum) : 
    Pending = 0
    Confirmed = 1
    OpenForLightning = 2
    Rejected = 3

class Notifications_ReadStatus_enum(Enum) :
    Unread = 0
    Read = 1

