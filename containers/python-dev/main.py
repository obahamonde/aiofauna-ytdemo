from datetime import datetime
from uuid import uuid4

from aiofauna import Api, ApiClient, FaunaModel, Field


class Demo(FaunaModel):
    uid:str = Field(default_factory=lambda:str(uuid4()))
    utime:str = Field(default_factory=datetime.now().isoformat)

app = Api()
client = ApiClient()

@app.get("/db")
async def db_insert():
    return await Demo().save()

@app.get("/api")
async def api_call():
    return await client.fetch("https://jsonplaceholder.typicode.com/posts")


@app.get("/")
async def index():
    return {
        "message": "Hello World!"
    }