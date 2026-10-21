"""Health check endpoint (Spring Boot gets the same from Actuator, including the db check)."""

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel
from sqlalchemy import Engine

from ecommerce.core.db import get_engine, is_database_up

router = APIRouter(tags=["health"])

Status = Literal["UP", "DOWN"]


class HealthResponse(BaseModel):
    status: Status
    # Individual checks, like Actuator's "components"
    components: dict[str, Status]


@router.get("/health", summary="Health check including the database")
def health(engine: Annotated[Engine, Depends(get_engine)], response: Response) -> HealthResponse:
    """UP when the database answers; otherwise DOWN with HTTP 503, like Actuator."""
    db: Status = "UP" if is_database_up(engine) else "DOWN"
    if db == "DOWN":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return HealthResponse(status=db, components={"db": db})
