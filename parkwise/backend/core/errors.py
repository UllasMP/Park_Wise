"""One error type for the whole API.

Raise ApiError anywhere; the @json_api decorator turns it into
{ "code": "...", "message": "..." } with the right HTTP status.
"""


class ApiError(Exception):
    def __init__(self, code, message, status=400):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status


# Fixed codes from the assessment sheet (code, HTTP status)
def invalid_vehicle(message):
    return ApiError("INVALID_VEHICLE", message, 422)


def already_parked():
    return ApiError("ALREADY_PARKED", "That vehicle is already inside.", 409)


def lot_full():
    return ApiError("LOT_FULL", "No free slot for this vehicle.", 409)


def not_parked():
    return ApiError("NOT_PARKED", "No vehicle or ticket found inside the lot.", 404)


def already_paid():
    return ApiError("ALREADY_PAID", "This ticket is already paid.", 409)


def bad_request(message):
    """Any other bad input -> 400 with a clear message."""
    return ApiError("BAD_REQUEST", message, 400)
