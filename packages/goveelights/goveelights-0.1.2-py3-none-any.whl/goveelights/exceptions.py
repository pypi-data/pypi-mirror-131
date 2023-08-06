"""
This is used to define all exceptions
"""


class GoveeException(Exception):
    """
    This is the base class for all exceptions thrown by this package.
    """


class ColorException(GoveeException):
    """
    This exception is used to indicate some issue occurred with a Color.
    """


class ColorAttributeException(GoveeException):
    """
    This exception is used to indicate some issue occurred with a Color Attr.
    """


class GoveeHubException(GoveeException):
    """
    This exception is used to indicate some issue occurred with a GoveeHub.
    """


class RefreshException(GoveeException):
    """
    This exception is used to indicate some issue occurred during a Device
    Refresh.
    """


class DeviceException(GoveeException):
    """
    This exception is used to indicate some issue occurred with a Device.
    """


class InvalidState(GoveeException):
    """
    This exception is used to indicate some issue occurred with a Device State.
    """


class InvalidValue(GoveeException):
    """
    This exception is used to indicate some issue occurred with a Device value.
    """


class ClientException(GoveeException):
    """
    This exception is used to indicate some issue occurred with a Govee Client.
    """


class InvalidAPIKey(GoveeException):
    """
    This exception is used to indicate some issue occurred with an API Key.
    """


class InvalidResponse(GoveeException):
    """
    This exception is used to indicate some issue occurred with a Govee Client.
    """
