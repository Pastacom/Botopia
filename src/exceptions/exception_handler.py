from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.exceptions.exceptions import BaseServiceException

app = FastAPI()


@app.exception_handler(BaseServiceException)
async def service_exception_handler(request: Request, exception: BaseServiceException):
    return JSONResponse(
        status_code=exception.status_code,
        content=exception.get_exception_details()
    )
