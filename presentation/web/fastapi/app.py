from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from application.ports.services.logger import LoggerPort
from infrastructure.config import get_redis_config
from infrastructure.config.cache import RedisConfig
from infrastructure.gateways.logging.factory import (
    create_console_json_logger,
)
from infrastructure.gateways.persistence.cache.redis.asynchronous.connection import (
    AsyncRedisConnection,
)
from presentation.web.fastapi.config import get_app_config
from presentation.web.fastapi.config.app import AppConfig
from presentation.web.fastapi.utils.exception_handlers_registry import (
    register_exception_handlers,
)
from presentation.web.fastapi.utils.routers_registry import register_routers

app_cfg: AppConfig = get_app_config()
redis_config: RedisConfig = get_redis_config()
logger: LoggerPort = create_console_json_logger()
redis_conn = AsyncRedisConnection(config=redis_config, logger=logger)


@asynccontextmanager
async def _lifespan(app: FastAPI):
    """
    FastAPI lifespan context: runs on startup and shutdown.
    Initializes resources (logger, Redis, etc.) and logs lifecycle events.
    """

    await redis_conn.connect()
    app.state.redis = redis_conn.client

    logger.info(f"[Lifespan] Starting {app_cfg.name} v{app_cfg.version}")

    register_routers(app, logger)
    logger.info("[AppFactory] FastAPI app fully configured")

    try:
        yield
    finally:
        logger.info(f"[Lifespan] Shutting down {app_cfg.name}")
        await redis_conn.disconnect()
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
    register_exception_handlers(app)

    return app
