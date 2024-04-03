from enum import Enum 
from sqlalchemy import Enum as EnumType

class Users_UserType_enum(Enum) : 
    Student = 0
    Manager = 1
    Administrator = 2

class SportSpaces_Type_enum(Enum) : 
    Tennis = 0
    Basketball = 1
    Soccer = 2

class Rentals_Status_enum(Enum) : 
    Pending = 0
    Confirmed = 1
    Rejected = 2

class RentalParticipants_Status_enum(Enum) : 
    Invited = 0
    Accepted = 1
    
class Friends_Status_enum(Enum) : 
    Pending = 0
    Accepted = 2

class ClubTimeSlots_DayOfWeek_enum(Enum) : 
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6

class ClubTimeSlots_Status_enum(Enum) : 
    Allocated = 0
    OpenForLightning = 1
