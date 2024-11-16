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
    
    
# static values, insert these in master_lists table
class Reactions:
    LOVE = '<i class="bi bi-suit-heart-fill text-danger"></i>'
    LIKE = '<i class="bi bi-hand-thumbs-up-fill text-success"></i>'
    ANGRY = '<i class="bi bi-emoji-angry-fill text-warning"></i>'
    SAD = '<i class="bi bi-emoji-frown-fill text-secondary"></i>'
    SMILE = '<i class="bi bi-emoji-grin-fill text-success"></i>'
    CARE = '<i class="bi bi-hearts text-danger"></i>'
    WOW = '<i class="bi bi-emoji-surprise-fill text-info"></i>'
    KISS = '<i class="bi bi-emoji-kiss-fill text-danger"></i>'
    HEARTBROKE = '<i class="bi bi-heartbreak-fill text-dark"></i>'