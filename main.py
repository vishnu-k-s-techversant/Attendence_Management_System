from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from database import ConnectToDatabase
from routers import router



app = FastAPI()

app.include_router(router)

ConnectToDatabase.connect(app)

