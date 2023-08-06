# encoding: utf-8


class CustomBaseError(Exception):
    def __init__(self, description=None):
        self.description = description
        self.status = None
        self.value = None

    def __str__(self):
        return 'Exception(status=%d, value=%s (description=%s))' % (self.status, self.value, self.description)

    # def __str__(self):
    #     return repr(self.value)


class InstructError(CustomBaseError):
    """
        This is Airtest CustomBaseError
    """
    pass


class UninstallApplicationError(CustomBaseError):
    """
        This is Airtest CustomBaseError
    """
    pass


class InstallApplicationError(CustomBaseError):
    """
        This is Airtest CustomBaseError
    """
    pass


class RestartDeviceError(CustomBaseError):
    """
        This is Airtest CustomBaseError
    """
    pass


class RejectException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Reject(value=%s)' % self.value


class NoDeviceAvailableException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'NoDeviceAvailable(value=%s)' % self.value
