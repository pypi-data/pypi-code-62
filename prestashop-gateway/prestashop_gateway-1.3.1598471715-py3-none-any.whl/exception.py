from .error import Error


class PrestashopWebServicesException(Error):
    ERROR_LABEL_1 = "This call to Prestashop Web Services failed and return an HTTP status of %d. That means %s"
    ERROR_LABEL_2 = (
        "This call to Prestashop Web Services returned an unexpected HTTP status of: %d"
    )
    MESSAGES = {
        204: "No content",
        400: "Bad request",
        401: "Unauthorized",
        404: "Not found",
        405: "Method not allowed",
        500: "Internal Server Error",
    }

    def __init__(self, status_code: int):
        self.status_code = status_code

        self.message = (
            self.ERROR_LABEL_1 % (status_code, self.MESSAGES.get(status_code))
            if status_code in [204, 400, 401, 404, 405, 500]
            else self.ERROR_LABEL_2 % status_code
        )


class PrestashopGatewayException(Exception):
    pass
