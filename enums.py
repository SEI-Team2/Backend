from enum import Enum 
from sqlalchemy import Enum as EnumType

class Users_UserType_enum(Enum) : 
    Student = 0
    Chairperson = 1
    Administrator = 2

class Friends_Status_enum(Enum) : 
    Pending = 0
    Accepted = 1
    Rejected = 2

class SportSpaces_Type_enum(Enum) : 
    TennisCourt = 0
    BasketballCourt = 1
    SoccerField = 2

class Rentals_Status_enum(Enum) : 
    Pending = 0
    Confirmed = 1
    Failed = 2
    Restricted = 3

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

class Clubmembers_Role_enum(Enum) :
    Member = 0
    Manager = 1

class ClubRentals_Dayofweek_enum(Enum) :
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6
