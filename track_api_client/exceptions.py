class ApiClientException(Exception):
    def __init__(self, method: str, message: str, details=None, response=None, request=None, *args, **kwargs):
        self.method = method
        self.message = message
        self.details = details
        self.response = response
        self.request = request
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        return 'Exception during calling method "{0}". Message: {1}. Details: {2}. Response: {3}'.format(
            self.method,
            self.message,
            self.details,
            self.response
        )

    def __str__(self) -> str:
        return self.__repr__()


class ApiClientUnauthorized(ApiClientException):
    pass


class ApiClientBadRequest(ApiClientException):
    pass
