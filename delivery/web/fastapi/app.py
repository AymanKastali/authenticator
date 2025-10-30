from contextlib import asynccontextmanager
from logging import Logger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from adapters.gateways.logging.logger_factory import create_logger_adapter
from application.ports.services.logger import LoggerPort
from delivery.web.fastapi.config import get_app_config
from delivery.web.fastapi.utils.exception_handlers_registry import (
    register_exception_handlers,
)
from delivery.web.fastapi.utils.routers_registry import register_routers

app_cfg = get_app_config()


@asynccontextmanager
async def _lifespan(app: FastAPI):
    """
    FastAPI lifespan context: runs on startup and shutdown.
    Attach logger or initialize other resources here.
    """
    logger: Logger = app.state.logger
    logger.info(f"[Lifespan] Starting {app_cfg.name} v{app_cfg.version}")

    # Place to initialize other resources (DB, caches, etc.)
    yield
    # Shutdown hooks
    logger.info(f"[Lifespan] Shutting down {app_cfg.name}")


def create_app() -> FastAPI:
    """
    Builds and configures the FastAPI application.
    """
    # --- Logger ---
    logger: LoggerPort = create_logger_adapter()

    # --- App instance ---
    app = FastAPI(
        title=app_cfg.name,
        version=app_cfg.version,
        debug=app_cfg.debug,
        lifespan=_lifespan,
    )
    app.state.logger = logger
    logger.info("[AppFactory] FastAPI app instance created")

    # --- Middleware ---
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --- Routers ---
    register_routers(app)
    logger.info("[AppFactory] Routers registered")

    # --- Exception handlers ---
    register_exception_handlers(app)
    logger.info("[AppFactory] Exception handlers registered")

    logger.info("[AppFactory] FastAPI app fully configured")
    return app
