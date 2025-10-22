from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from delivery.web.fastapi.utils.exception_handlers_registry import (
    register_exception_handlers,
)
from delivery.web.fastapi.utils.routers_registry import register_routers


def create_app() -> FastAPI:
    """
    Initialize and configure the FastAPI application.
    """
    app = FastAPI(
        title="Authenticator Service API",
        version="1.0.0",
        # default_response_class=SuccessJSONResponse,
    )

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify allowed origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_routers(app)
    register_exception_handlers(app)

    return app
