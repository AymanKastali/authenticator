from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from adapters.startup.manager import ResourceManager
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
    Initializes resources (logger, Redis, etc.) and logs lifecycle events.
    """
    # Initialize resources
    manager = ResourceManager()
    await manager.initialize()

    # Attach logger to app state
    app.state.resources = manager
    logger: LoggerPort = manager.logger

    # Startup logs
    logger.info(f"[Lifespan] Starting {app_cfg.name} v{app_cfg.version}")
    logger.info("[AppFactory] FastAPI app instance created")

    # Initialize routers, exception handlers, and any other startup tasks
    register_routers(app, logger)
    logger.info("[AppFactory] Routers registered")

    register_exception_handlers(app)
    logger.info("[AppFactory] Exception handlers registered")

    logger.info("[AppFactory] FastAPI app fully configured")

    # Yield control back to FastAPI (app runs here)
    try:
        yield
    finally:
        # Shutdown resources
        logger.info(f"[Lifespan] Shutting down {app_cfg.name}")
        await manager.shutdown()
        logger.info("[ResourceManager] All resources disconnected")


def create_app() -> FastAPI:
    """
    Builds and configures the FastAPI application.
    """
    # --- App instance ---
    app = FastAPI(
        title=app_cfg.name,
        version=app_cfg.version,
        debug=app_cfg.debug,
        lifespan=_lifespan,
    )

    # --- Middleware ---
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
