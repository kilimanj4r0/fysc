from fastapi import FastAPI
from routers import detector


app = FastAPI()
app.include_router(detector.router)

@app.get("/")
def hello_world():
    return {"Hello": "World"}
