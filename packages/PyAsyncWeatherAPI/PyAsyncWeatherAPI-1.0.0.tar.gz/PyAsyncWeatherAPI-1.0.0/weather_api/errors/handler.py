import json
from typing import Any

from .errors import (
    APIKeyNotProvided,
    LocationNotProvided,
    URLInvalid,
    NoLocationFound,
    APIKeyInvalid,
    APIKeyCallsExceeded,
    APIKeyIsDisabled,
    InternalApplicationError
)


class ErrorHandler:
    @staticmethod
    def check(response: str) -> Any:
        data = json.loads(response)

        if "error" not in data:
            return data

        error_code = data["error"]["code"]

        if error_code == 1002:
            raise APIKeyNotProvided("API key not provided.")

        if error_code == 1003:
            raise LocationNotProvided("Parameter 'q' not provided.")

        if error_code == 1005:
            raise URLInvalid("API request url is invalid.")

        if error_code == 1006:
            raise NoLocationFound("No location found matching parameter 'q'.")

        if error_code == 2006:
            raise APIKeyInvalid("API key provided is invalid.")

        if error_code == 2007:
            raise APIKeyCallsExceeded("API key has exceeded calls per month quota.")

        if error_code == 2008:
            raise APIKeyIsDisabled("API key has been disabled.")

        if error_code == 9999:
            raise InternalApplicationError("Internal application error.")
