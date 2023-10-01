from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_origin_regex="https:\/\/.*\.uffizzi\.com",
    allow_methods=["GET", "POST", "PUT", "DELETE", "UPDATE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get('/')
def index():
    return {"msg": "home"}