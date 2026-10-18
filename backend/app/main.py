from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.identity.router import router as identity_router
from app.vault.router import router as vault_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings = get_settings()
    # Hard fail if someone tries to enable dev auth in deployed envs.
    if settings.environment in ("production", "staging") and (
        settings.auth_mode == "dev" or settings.auth_dev_mode
    ):
        raise RuntimeError("Refusing to start: dev authentication enabled in non-development environment")
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )
    app.include_router(identity_router, prefix=settings.api_prefix)
    app.include_router(vault_router, prefix=settings.api_prefix)

    @app.get("/health")
    def health():
        return {
            "status": "ok",
            "environment": settings.environment,
            "auth_mode": settings.auth_mode,
        }

    return app


app = create_app()
