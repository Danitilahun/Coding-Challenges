from fastapi.responses import JSONResponse
from fastapi import HTTPException


class ErrorHandler:

    @staticmethod
    def json_response(message: str, status_code: int = 400) -> JSONResponse:
        """
        Generates a JSON response with a custom error message and status code.

        Args:
            message (str): The error message to include in the response.
            status_code (int): The HTTP status code for the response. Default is 400.

        Returns:
            JSONResponse: A JSON response object.
        """
        return JSONResponse(content={"message": message}, status_code=status_code)

    @staticmethod
    def raise_exception(message: str, status_code: int = 400):
        """
        Raises an HTTPException with a custom message and status code.

        Args:
            message (str): The error message to include in the exception.
            status_code (int): The HTTP status code for the exception. Default is 400.

        Raises:
            HTTPException: A FastAPI HTTPException.
        """
        raise HTTPException(status_code=status_code,
                            detail={"message": message})
