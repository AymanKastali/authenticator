from fastapi import FastAPI

from delivery.web.fastapi.exception_handlers.registry import EXCEPTION_HANDLERS


def register_exception_handlers(app: FastAPI):
    """
    Register all exception handlers from EXCEPTION_HANDLERS to the FastAPI app.
    """
    for exc_type, handler in EXCEPTION_HANDLERS.items():
        app.add_exception_handler(exc_type, handler)
