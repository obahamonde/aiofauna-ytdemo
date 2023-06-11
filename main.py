from aiofauna import render_template

from api.controller import app
from api.repository import CodeServer, DatabaseKey, PythonContainer, User


@app.get("/")
async def index():
    return {
        "message": "Welcome to the Python Playground!",
    }

app.static()

#@app.on_event("startup")
async def startup(_):
    await DatabaseKey.provision()
    await User.provision()
    await PythonContainer.provision()
    await CodeServer.provision()


if __name__ == "__main__":
    app.run(port=8080)