from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
import logging

try:  # works in Python >= 3.3
    import collections.abc as collections_abc
except ImportError:  # Python <= 3.2 including Python 2
    import collections as collections_abc


async def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    print([request.url, request.method, exc.status_code, exc.detail])
    logging.info([request.url, request.method, exc.status_code, exc.detail])
    return JSONResponse({"errors": [f'{exc.status_code} {exc.detail}']}, status_code=exc.status_code)


async def http_422_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handler for 422 error to transform default pydnatic error obejct to gothinkster format
    """
    errors = {"body": []}

    if isinstance(exc.detail, collections_abc.Iterable) and not isinstance(
            exc.detail, str
    ):
        for error in exc.detail:
            error_name = ".".join(
                error["loc"][1:]
            )  # remove 'body' from path to invalid element
            errors["body"].append({error_name: error["msg"]})
    else:
        errors["body"].append(exc.detail)
    print(errors)
    return JSONResponse({"result": None, 'message': 'Unprocessable entity', 'code': 422},
                        status_code=HTTP_422_UNPROCESSABLE_ENTITY)