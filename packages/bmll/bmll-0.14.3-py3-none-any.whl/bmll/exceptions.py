

class AuthenticationError(Exception):
    """The service was unable to authenticate."""
    pass


class LoginError(Exception):
    """An error has occurred when attempting to login to the BMLL Services."""
    pass


class MarketDataError(Exception):
    """Failed to retrieve market data."""
    pass
