from typing import Union
from pydantic import BaseModel
from pymongo import MongoClient
from openai import OpenAI
from fastapi import FastAPI
from app.routers.threads import router as threads_router

app = FastAPI()

# Include the threads router
app.include_router(threads_router)
