

class BaseServiceException(Exception):
    def __init__(self, status_code: int, message: str = "", meta: dict | None = None):
        self.status_code = status_code
        self.message = message

        if meta is None:
            meta = {}

        self.meta = meta

        super().__init__(message)

    def get_exception_details(self) -> dict:
        return {"message": self.message, "meta": self.meta}


class UserAlreadyExistsException(BaseServiceException):
    def __init__(self, message: str = "", meta: dict | None = None):
        super().__init__(409, message, meta)


class UserNotFoundException(BaseServiceException):
    def __init__(self, message: str = "", meta: dict | None = None):
        super().__init__(404, message, meta)


class UserIsAlreadyLockedException(BaseServiceException):
    def __init__(self, message: str = "", meta: dict | None = None):
        super().__init__(409, message, meta)
