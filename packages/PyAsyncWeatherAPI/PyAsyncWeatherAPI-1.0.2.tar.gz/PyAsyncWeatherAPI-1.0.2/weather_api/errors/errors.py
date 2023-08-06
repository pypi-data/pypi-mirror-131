class APIKeyNotProvided(Exception):
    pass


class LocationNotProvided(Exception):
    pass


class URLInvalid(Exception):
    pass


class NoLocationFound(Exception):
    pass


class APIKeyInvalid(Exception):
    pass


class APIKeyCallsExceeded(Exception):
    pass


class APIKeyIsDisabled(Exception):
    pass


class InternalApplicationError(Exception):
    pass
