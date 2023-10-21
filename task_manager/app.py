from fastapi import FastAPI

from task_manager.routes import auth, users

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)


@app.get('/')
def read_root():
    return {'message': 'Hello, world!'}
