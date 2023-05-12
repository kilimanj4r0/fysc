from fastapi import FastAPI
from routers import detector
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(detector.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def hello_world():
    return {"Hello": "World"}
