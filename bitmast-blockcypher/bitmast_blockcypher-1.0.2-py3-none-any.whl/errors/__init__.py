from requests.exceptions import RequestException


class BaseError(RequestException):
    """ Base error for the application """
    def __init__(self, *args, **kwargs):
        self._error = kwargs.get('error')
        self._request_id = kwargs.get('requestId')
        self._context = kwargs.get('context')
        self._name = kwargs.get('name')
        super(BaseError, self).__init__(*args, **kwargs)

    @property
    def error(self):
        return self._error

    @property
    def request_id(self):
        return self._request_id

    @property
    def context(self):
        return self._context

    @property
    def name(self):
        return self._name


class AuthorizationError(BaseError):
    """ Access to the gateway was not authorized """


class ApiKeyError(BaseError):
    """ Merchant key was not valid """


class InvalidDataError(BaseError, ValueError):
    """ Data to or from gateway was malformed or invalid """


class HttpResponseError(BaseError):
    """ Response error for the application API call """


class InvalidCoin(BaseError, ValueError):
    """ Base error for invalid coin requests """


class CustodialWalletLimitReachedError(BaseError):
    pass


class MustHaveColdWalletLicenseError(BaseError):
    pass


class MustHaveCustodialWalletLicenseError(BaseError):
    pass


class WalletError(BaseError):
    """Base error for all invalid wallet operation or state"""


class WalletLimitReachedError(WalletError):
    pass


class InvalidWalletError(WalletError):
    """Raised error if the wallet id is invalid or some required wallet parameter is invalid"""


class WalletHasNonZeroBalanceError(WalletError):
    """ Raised error if the wallet is owned by single user and does not have 0 unit balance """


class InvalidEnterpriseError(BaseError):
    """Raised for when an invalid enterprise id or identifier is supplied"""


class WalletCountError(WalletError):
    """Raised if wallet count exceeds 500"""


class WalletNotFoundError(WalletError):
    """Raised when wallet is not found"""


class CoinError(BaseError):
    """Raised when an operation is performed on unknown or unsupported coin"""
