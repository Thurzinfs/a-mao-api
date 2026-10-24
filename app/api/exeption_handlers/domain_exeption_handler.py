from fastapi import Request
from fastapi.responses import JSONResponse

from config.exception import BaseDomainException


async def domain_exeption_handler(request: Request, exc: BaseDomainException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )
