from fastapi import FastAPI
from app.api.users import router as user_router
from app.api.posts import router as post_router
from app.api.swagger import router as swagger_router


def create_app() -> FastAPI:
    app = FastAPI(title='Starnavi')
    app.include_router(user_router, prefix='/api/v1/users')
    app.include_router(post_router, prefix='/api/v1/posts')
    app.include_router(swagger_router)
    return app


app = create_app()
