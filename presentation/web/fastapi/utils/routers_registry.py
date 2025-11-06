from fastapi import FastAPI
from fastapi.routing import APIRoute

from application.ports.services.logger import LoggerPort
from presentation.web.fastapi.api.v1.router import v1_router


def register_routers(app: FastAPI, logger: LoggerPort):
    app.include_router(v1_router)

    routes_info = [
        {"path": route.path, "methods": list(route.methods), "name": route.name}
        for route in app.routes
        if isinstance(route, APIRoute)
    ]

    logger.info("Registered all routes", extra={"routes": routes_info})
