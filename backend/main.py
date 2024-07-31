from fastapi import FastAPI

from api.router import router


# uvicorn main:init_app --reload --log-config=log_conf.yaml
def init_app() -> FastAPI:
    application = FastAPI(title="Patient Record Management API")
    application.include_router(router)
    return application