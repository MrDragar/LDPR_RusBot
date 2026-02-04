from fastapi import FastAPI
from src.application.routes import root_router

app = FastAPI()
app.include_router(root_router)
