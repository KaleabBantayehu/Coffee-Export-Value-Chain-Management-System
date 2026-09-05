from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from jose import JWTError

from app.api.v1.auth import router as auth_router
from app.api.v1.farms import router as farms_router
from app.api.v1.farmers import router as farmers_router
from app.api.v1.lots import router as lots_router
from app.api.v1.qr import router as qr_router
from app.api.v1.users import router as users_router


def create_app() -> FastAPI:
    app = FastAPI(title="CEVCMS Backend")
    app.include_router(auth_router, prefix="/api/v1")
    app.include_router(users_router, prefix="/api/v1")
    app.include_router(farmers_router, prefix="/api/v1")
    app.include_router(farms_router, prefix="/api/v1")
    app.include_router(lots_router, prefix="/api/v1")
    app.include_router(qr_router, prefix="/api/v1")

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Malformed request body."},
        )

    @app.exception_handler(JWTError)
    async def jwt_error_handler(_: Request, exc: JWTError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid authentication token."},
        )

    @app.get("/api/v1/health", response_class=JSONResponse)
    async def health_check():
        return {"status": "ok", "version": "v1"}

    return app


app = create_app()
