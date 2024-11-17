class EmailTemplate:
    def __init__(self, subject: str, message: str) -> None:
        self.__subject = subject
        self.__message = message

    def get_subject(self, **kwargs) -> str:
        subject = self.__subject
        for key, value in kwargs.items():
            subject = subject.replace(f"{{{key}}}", str(value))
        return subject

    def get_message(self, **kwargs) -> str:
        message = self.__message
        for key, value in kwargs.items():
            message = message.replace(f"{{{key}}}", str(value))
        return message
