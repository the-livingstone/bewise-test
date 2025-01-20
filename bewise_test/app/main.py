import asyncio
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

import app.config as config
from app.routes import router
from app.errors import RepresentativeError
from app.db.base import Base, engine
from bewise_test.app.messages import KafkaPublisher

async def create_tables() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.producer = KafkaPublisher(bootstrap_servers=[f"{config.KAFKA_SERVER}:{config.KAFKA_PORT}"])
    await app.state.producer.start()
    yield
    await app.state.producer.stop()


def get_app() -> FastAPI:
    docs_url = "/_docs" if config.DEBUG else None
    app = FastAPI(
        title="Walk the dog",
        debug=config.DEBUG,
        docs_url=docs_url,
        lifespan=lifespan,
    )
    app.include_router(router)

    @app.exception_handler(RepresentativeError)
    def ex_handler(request, ex: RepresentativeError):
        return JSONResponse(status_code=ex.status_code, content=ex.dict())

    return app


if __name__ == "__main__":
    asyncio.run(create_tables())

    uvicorn.run(
        "app.main:get_app",
        factory=True,
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True,
    )
