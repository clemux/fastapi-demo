"""Custom exceptions"""


class WrongLoginException(Exception):
    """Raised when the login or password is wrong."""


class EmailAlreadyExistsException(Exception):
    """Raised when the email already exists when attempting to register."""


class EmailServiceError(Exception):
    """Raised when the email service is not available."""


class UserNotFoundException(Exception):
    """Raised when the user is not found"""


class InvalidActivationCodeException(Exception):
    """Raised when the activation code is invalid"""
