import os
from datetime import datetime
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import FastAPI
from faunadb import query as q
from faunadb.client import FaunaClient
from httpx import AsyncClient
from pydantic import BaseModel, Field

load_dotenv()

FAUNA_SECRET=os.getenv("FAUNA_SECRET")

db = FaunaClient(secret=FAUNA_SECRET)

async def fetch(url):
    async with AsyncClient() as client:
        response = await client.get(url)
        return response.json()

class Demo(BaseModel):
    uid:str = Field(default_factory=lambda:str(uuid4()))
    utime:str = Field(default_factory=datetime.now().isoformat)

    def save(self):
        json_response = db.query(q.create(q.collection("demo"), {"data": self.dict()}))
        return {
            "ref": json_response["ref"].id(),
            "ts": json_response["ts"],
            **json_response["data"]
        }
        
app = FastAPI()

@app.get("/db")
async def db_insert():
    return Demo().save()

@app.get("/api")
async def api_call():
    return await fetch("https://jsonplaceholder.typicode.com/posts")

