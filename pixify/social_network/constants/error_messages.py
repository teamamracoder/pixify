from enum import Enum


class ErrorMessage(Enum):
    E000001 = "Login failed, please try again"
    E000002 = "OTP expired"
    E000003 = "OTP send failed, please try again"
    E000004 = "Invalid OTP or OTP expired"
    E000005 = "no chats available"
