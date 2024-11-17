from abc import abstractmethod
from social_network.constants.default_values import (
    ResponseMessageType,
)


def success_response(
    message: str,
    data: dict = dict(),
    message_type: str = ResponseMessageType.SUCCESS.value,
) -> dict:
    return {
        "success": True,
        "data": data,
        "message_type": message_type,
        "message": message,
    }


def error_response(
    message: str,
    data: dict = dict(),
    message_type: str = ResponseMessageType.ERROR.value,
    stack_trace: str = "",
) -> dict:
    return {
        "error": True,
        "data": data,
        "message": message,
        "message_type": message_type,
        "stack_trace": stack_trace,
    }
