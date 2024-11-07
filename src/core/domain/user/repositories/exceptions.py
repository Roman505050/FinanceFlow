from core.shared.exceptions import NotFoundException, AlreadyExistsException


class UserNotFoundException(NotFoundException):
    pass


class UserAlreadyExistsException(AlreadyExistsException):
    pass
