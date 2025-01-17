from enum import Enum

class Role(Enum):
    ADMIN = 1
    END_USER = 2

class Gender(Enum):
    MALE = 1
    FEMALE = 2
    OTHER = 3

class PostType(Enum):
    NORMAL = 1
    STATUS = 2
    SHOTS = 3

class PostContentType(Enum):
    TEXT = 1
    PHOTO = 2
    VIDEO = 3

class AccessLevel(Enum):
    PRIVATE = 1
    FOLLOWER = 2
    PUBLIC = 3

class SpecificUserTreatment(Enum):
    INCLUDE = 1
    EXCLUDE = 2

class ChatType(Enum):
    PERSONAL = 1
    GROUP = 2

class RelationShipStatus(Enum):
    SINGLE = 1
    MARRIED = 2
    DIVORCED = 3
    COMMITTED = 4
    
class MasterType(Enum):
    REACTION = 1


class ResponseMessageType(Enum):
    SUCCESS='success'
    ERROR='error'
    WARNING='warning'
    INFO='info'
    NONE='null'

class SortingOrder(Enum):
    ASC='asc',
    DESC='desc'
    
class UIMODES(Enum):
    LIGHT=1
    DARK=2

# static values, insert these in master_lists table
class Reactions:
    LOVE = '<i class="fa-solid fa-heart" style="color: #eb0505;"></i>'
    LIKE = '<i class="fa-solid fa-thumbs-up" style="color: #ffec1a;"></i>'
    ANGRY = '<i class="fa-solid fa-face-angry" style="color: #ff0a0a;"></i>'
    SAD = '<i class="fa-solid fa-face-sad-tear" style="color: #ffcb0f;"></i>'
    SMILE = '<i class="fa-solid fa-face-smile-beam" style="color: #FFD43B;"></i>'
    WOW = '<i class="fa-solid fa-face-surprise" style="color: #FFD43B;"></i>'
    KISS = '<i class="fa-solid fa-face-kiss-beam" style="color: #FFD43B;"></i>'
    HEARTBROKE = '<i class="fa-solid fa-heart-crack" style="color: #d40202;"></i>'
    FAKESMILE= '<i class="fa-solid fa-face-grin-beam-sweat" style="color: #FFD43B;"></i>'

class MessageDeleteType(Enum):
    NOT_DELETED = 1    
    DELETED_FOR_EVERYONE = 2