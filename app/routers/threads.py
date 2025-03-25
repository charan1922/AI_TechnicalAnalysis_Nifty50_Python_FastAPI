from fastapi import APIRouter, HTTPException
from app.core.database import get_database

# from openai import OpenAI

# client = OpenAI()
db = get_database()
router = APIRouter(prefix="/threads", tags=["threads"])

collection = db["threads"]


@router.get("/new")
async def create_thread():
    return {"threadId": "", "analysisName": ""}
