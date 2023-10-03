from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import Base, engine
from api.routes.user import user_router
from api.routes.auth import auth_router
from api.routes.post import post_router
from api.routes.event import event_router
from api.routes.announcements import announcement_router
from api.routes.communities import community_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(post_router)
app.include_router(event_router)
app.include_router(announcement_router)
app.include_router(community_router)

@app.get("/")
def root():
    return {"message": "Hello World"}