from config.exception import BaseDomainException


class UserNotFoundException(BaseDomainException):
    message = "User not found"
    status_code = 404


class UserAlreadyExistsException(BaseDomainException):
    message = "User already exists"
    status_code = 400
