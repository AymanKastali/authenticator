from fastapi import FastAPI

from delivery.web.fastapi.api.v1.router import v1_router


def register_routers(app: FastAPI):
    """
    Register all FastAPI routers here.
    """
    app.include_router(v1_router)
