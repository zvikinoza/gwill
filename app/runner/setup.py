from fastapi import FastAPI
from app.core import goodwillAPI
from app.infra.api import goodwill
from app.infra.in_mem import ProductRepo


# uvicorn app.runner.asgi:app --reload
# http://localhost:8000/docs
def setup() -> FastAPI:
    app = FastAPI()
    app.include_router(goodwill)
    app.state.core = goodwillAPI(product_repo=ProductRepo())
    return app
