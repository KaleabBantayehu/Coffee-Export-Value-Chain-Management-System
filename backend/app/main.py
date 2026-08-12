from fastapi import FastAPI
from starlette.responses import JSONResponse


def create_app() -> FastAPI:
    app = FastAPI(title="CEVCMS Backend")

    @app.get("/api/v1/health", response_class=JSONResponse)
    async def health_check():
        return {"status": "ok", "version": "v1"}

    return app


app = create_app()
