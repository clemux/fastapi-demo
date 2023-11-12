"""Custom exceptions"""


class WrongLoginException(Exception):
    """Raised when the login or password is wrong"""


class EmailAlreadyExistsException(Exception):
    """Raised when the email already exists when attempting to register"""
