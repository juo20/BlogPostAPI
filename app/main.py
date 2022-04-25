from fastapi import FastAPI
# from . import models
# from .database import engine
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# This tells sqlalchemy to create all tables listed in models.py
# which is no longer needed as alembic is doing the db migrations
# models.Base.metadata.create_all(bind=engine)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)