import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

import app.config as config
from app.routes import router
from app.errors import RepresentativeError


def get_app() -> FastAPI:
    docs_url = "/_docs" if config.DEBUG else None
    app = FastAPI(
        title="Walk the dog",
        debug=config.DEBUG,
        docs_url=docs_url,
    )
    app.include_router(router)

    @app.exception_handler(RepresentativeError)
    def ex_handler(request, ex: RepresentativeError):
        return JSONResponse(status_code=ex.status_code, content=ex.dict())

    return app


if __name__ == "__main__":
    uvicorn.run(
        "app.main:get_app",
        factory=True,
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True,
    )
