from enum import Enum 
from sqlalchemy import Enum as EnumType

class Users_UserType_enum(Enum) : 
    Student = 0
    Clubmanager = 1
    Administrator = 2

class Friends_Status_enum(Enum) : 
    Pending = 0
    Accepted = 1
    Rejected = 2

class SportSpaces_Type_enum(Enum) : 
    TennisCourt = 0
    BasketballCourt = 1
    SoccerField = 2

class Rentals_Types_enum(Enum) : 
    Light = 0
    Club = 1
    Restrict = 2

class Rentals_Status_enum(Enum) : 
    Open = 0
    Half = 1
    Close = 2

class Rentals_Flags_enum(Enum) : 
    Fix = 0
    Nonfix = 1

class RentalParticipants_Status_enum(Enum) : 
    Invited = 0
    Accepted = 1

class Notifications_ReadStatus_enum(Enum) :
    Unread = 0
    Read = 1

class Notifications_Types_enum(Enum) :
    rental_fix = 0
    rental_cancle = 1
    friend_request = 2
    friend_accept = 3
    friend_reject = 4
    club_member_add = 5
    club_member_delete = 6
    club_manager_add = 7
    club_manager_delete = 8

class ClubRentals_Dayofweek_enum(Enum) :
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6

class Clubmembers_Role_enum(Enum) :
    Member = 0
    Manager = 1