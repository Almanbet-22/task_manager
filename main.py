from router import router as tasks_router
from auth_router import router as auth_router
from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("База данных готова к работе")

    yield

    print("Выключение сервера")

app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)
app.include_router(auth_router)