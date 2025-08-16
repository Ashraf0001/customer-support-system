from fastapi import APIRouter
from fastapi.responses import RedirectResponse, PlainTextResponse

from app.api import endpoint
from app.api import customer_support_endpoint

"""
API Router Module

This module sets up the API router and includes all defined endpoints.
It uses FastAPI's APIRouter to group related endpoints and provide a prefix.
"""

router = APIRouter()


@router.get("/healthz", include_in_schema=False)
def healthz():
    return PlainTextResponse("ok")


@router.get("/readyz", include_in_schema=False)
def readyz():
    # Basic readiness probe
    return PlainTextResponse("ready")


@router.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

router.include_router(endpoint.router, prefix="/events", tags=["events"])
router.include_router(customer_support_endpoint.router, prefix="/support", tags=["customer-support"])
