# coding:utf-8

class CustomBaseException(Exception):
    def __init__(self, message):
        super().__init__(self)
        self.error = message


class NetworkException(CustomBaseException):
    pass


class UserNotFoundException(CustomBaseException):
    pass
