class RobotError(Exception):
    """Base class for all robot errors."""
    pass

class RobotConnectionError(RobotError):
    """Connection to robot failed."""
    pass

class RobotTimeoutError(RobotError):
    """Robot did not answer in time."""
    pass

class RobotProtocolError(RobotError):
    """Unexpected robot response."""
    pass