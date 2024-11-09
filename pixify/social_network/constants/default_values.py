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