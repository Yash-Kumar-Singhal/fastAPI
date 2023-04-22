from fastapi import FastAPI
from app import model
from .database import engine
from .routers import post,user,auth,vote
from .config import setting
from fastapi.middleware.cors import CORSMiddleware


#  we do not need this as we are using alembic for database creation
# this is use to auto generate table whenever we use to save our script however the problem was if table name match then 
# doesnt uodate the table column or any value we have changed

# model.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


 