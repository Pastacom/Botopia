from fastapi import FastAPI
import uvicorn

from src.handlers.v1 import users_handler, lock_handler
from src.exceptions.exceptions import BaseServiceException
from src.exceptions.exception_handler import service_exception_handler

app = FastAPI(title="Botopia Service")

app.include_router(users_handler.router, prefix="/api/v1")
app.include_router(lock_handler.router, prefix="/api/v1")
app.add_exception_handler(BaseServiceException, service_exception_handler)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
