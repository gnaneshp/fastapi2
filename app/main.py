from fastapi import FastAPI
from app.routers import post,user,auth,vote
from random import randrange
from app import models
from app.database import engine,get_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(post.app)
app.include_router(user.app)
app.include_router(auth.app)
app.include_router(vote.app)
# models.Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Welcolme to my API "}

