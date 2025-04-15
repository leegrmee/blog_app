from fastapi import HTTPException, status


class AppException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class NotFoundException(AppException):
    def __init__(self, name: str):
        detail = f"{name} not found."
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class PermissionDeniedException(AppException):
    def __init__(self, detail: str = "Permission denied."):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class BadRequestException(AppException):
    def __init__(self, detail: str = "Bad request."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ConflictException(AppException):
    def __init__(self, detail: str = "Conflict occurred."):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class DatabaseException(AppException):
    def __init__(self, detail: str = "Database error."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )


class InternalServerException(AppException):
    def __init__(self, detail: str = "Internal server error."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )


class InvalidInputException(AppException):
    def __init__(self, detail: str = "Invalid input."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
