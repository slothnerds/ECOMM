"""One error format for the whole API, produced centrally (the counterpart of core/error in Java).

Every failure becomes the same JSON body as in the Java app:
{code, message, status, path, timestamp, fieldErrors}. Endpoints never build error responses;
they raise, and the handlers registered by register_error_handlers() do the rest.
"""

import logging
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import StaleDataError
from starlette.exceptions import HTTPException as StarletteHTTPException

from ecommerce.core.api import ApiModel, Messages

logger = logging.getLogger("uvicorn.error")


class ErrorCode(StrEnum):
    """Stable, machine-readable codes; the same as ErrorCode.java."""

    VALIDATION_FAILED = "VALIDATION_FAILED"
    MALFORMED_REQUEST = "MALFORMED_REQUEST"
    NOT_FOUND = "NOT_FOUND"
    METHOD_NOT_ALLOWED = "METHOD_NOT_ALLOWED"
    PRODUCT_NOT_FOUND = "PRODUCT_NOT_FOUND"
    DUPLICATE_SKU = "DUPLICATE_SKU"
    CONCURRENT_UPDATE = "CONCURRENT_UPDATE"
    CONFLICT = "CONFLICT"
    INTERNAL_ERROR = "INTERNAL_ERROR"


HTTP_STATUS: dict[ErrorCode, int] = {
    ErrorCode.VALIDATION_FAILED: 400,
    ErrorCode.MALFORMED_REQUEST: 400,
    ErrorCode.NOT_FOUND: 404,
    ErrorCode.METHOD_NOT_ALLOWED: 405,
    ErrorCode.PRODUCT_NOT_FOUND: 404,
    ErrorCode.DUPLICATE_SKU: 409,
    ErrorCode.CONCURRENT_UPDATE: 409,
    ErrorCode.CONFLICT: 409,
    ErrorCode.INTERNAL_ERROR: 500,
}


class BusinessError(Exception):
    """Parent of every expected business error; carries its code (like BusinessException.java)."""

    code: ErrorCode = ErrorCode.INTERNAL_ERROR

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class FieldError(ApiModel):
    field: str
    message: str


class ApiError(ApiModel):
    """The one error body of the API, identical to ApiError.java."""

    code: ErrorCode
    message: str
    status: int
    path: str
    timestamp: str  # UTC with milliseconds and Z, like Java's Instant truncated to millis
    field_errors: list[FieldError]


def error_response(
    code: ErrorCode, message: str, request: Request, fields: list[FieldError] | None = None
) -> JSONResponse:
    now = datetime.now(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    body = ApiError(
        code=code,
        message=message,
        status=HTTP_STATUS[code],
        path=request.url.path,
        timestamp=now,
        # Stable order, so responses (and tests) don't depend on validation order
        field_errors=sorted(fields or [], key=lambda f: (f.field, f.message)),
    )
    return JSONResponse(
        status_code=body.status, content=body.model_dump(mode="json", by_alias=True)
    )


# ---------------------------------------------------------------------------------------------
# Translating Pydantic validation errors into the shared field messages
# ---------------------------------------------------------------------------------------------

_DECIMAL_LIMITS = {"decimal_max_digits", "decimal_max_places", "decimal_whole_digits"}
_MALFORMED_TYPES = {"json_invalid", "model_attributes_type", "dict_type"}


def _field_message(error: dict[str, Any]) -> str:
    kind: str = error["type"]
    ctx: dict[str, Any] = error.get("ctx") or {}
    if kind == "missing" or (kind.endswith("_type") and error.get("input") is None):
        return Messages.REQUIRED  # absent, or sent as null
    if kind == "string_too_long":
        return f"must be at most {ctx['max_length']} characters"
    if kind == "greater_than":
        return f"must be greater than {ctx['gt']}"
    if kind == "greater_than_equal":
        return f"must be greater than or equal to {ctx['ge']}"
    if kind == "less_than_equal":
        return f"must be less than or equal to {ctx['le']}"
    if kind in _DECIMAL_LIMITS:
        return Messages.MONEY_DIGITS
    if kind == "enum":
        # ctx["expected"] looks like "'DRAFT', 'ACTIVE' or 'DISCONTINUED'"
        allowed = ctx["expected"].replace("'", "").replace(" or ", ", ")
        return f"must be one of {allowed}"
    if kind == "value_error":
        # Our own validators (blank name, SKU format) raise ValueError(<shared message>)
        return str(error["msg"]).removeprefix("Value error, ")
    return Messages.INVALID_VALUE


def _is_malformed(errors: list[dict[str, Any]]) -> bool:
    """The body as a whole is missing or isn't a JSON object (not a problem with one field)."""
    return any(e["type"] in _MALFORMED_TYPES or tuple(e["loc"]) == ("body",) for e in errors)


# ---------------------------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------------------------


def register_error_handlers(app: FastAPI) -> None:
    """Install the central handlers (the counterpart of @RestControllerAdvice)."""

    @app.exception_handler(BusinessError)
    async def business(request: Request, exc: BusinessError) -> JSONResponse:
        return error_response(exc.code, exc.message, request)

    @app.exception_handler(RequestValidationError)
    async def invalid_request(request: Request, exc: RequestValidationError) -> JSONResponse:
        errors = list(exc.errors())
        if _is_malformed(errors):
            return error_response(
                ErrorCode.MALFORMED_REQUEST,
                "Request body is missing or is not valid JSON",
                request,
            )
        fields = [FieldError(field=str(e["loc"][-1]), message=_field_message(e)) for e in errors]
        return error_response(
            ErrorCode.VALIDATION_FAILED, "Request validation failed", request, fields
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_error(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        """Routing errors raised by the framework: unknown URL (404), wrong method (405)."""
        if exc.status_code == 405:
            return error_response(
                ErrorCode.METHOD_NOT_ALLOWED,
                f"Method {request.method} is not allowed for {request.url.path}",
                request,
            )
        if exc.status_code == 404:
            return error_response(
                ErrorCode.NOT_FOUND, f"No endpoint {request.method} {request.url.path}", request
            )
        logger.warning("Unmapped HTTP error %s on %s", exc.status_code, request.url.path)
        return error_response(ErrorCode.INTERNAL_ERROR, "An unexpected error occurred", request)

    @app.exception_handler(StaleDataError)
    async def concurrent_update(request: Request, exc: StaleDataError) -> JSONResponse:
        return error_response(
            ErrorCode.CONCURRENT_UPDATE,
            "The data was changed by another request; reload it and try again",
            request,
        )

    @app.exception_handler(IntegrityError)
    async def constraint_violated(request: Request, exc: IntegrityError) -> JSONResponse:
        logger.warning("Constraint violation on %s: %s", request.url.path, exc.orig)
        return error_response(
            ErrorCode.CONFLICT, "The request conflicts with existing data", request
        )

    @app.exception_handler(Exception)
    async def unexpected(request: Request, exc: Exception) -> JSONResponse:
        """Anything unexpected: full details go to the log only, never to the client."""
        logger.error("Unexpected error on %s %s", request.method, request.url.path, exc_info=exc)
        return error_response(ErrorCode.INTERNAL_ERROR, "An unexpected error occurred", request)
