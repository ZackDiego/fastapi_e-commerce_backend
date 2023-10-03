from fastapi import FastAPI
from . import models, config
from .database import engine
from .routers import products, users, auth, ratings


# model create engine
# models.Base.metadata.create_all(bind = engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(products.router)
app.include_router(auth.router)
app.include_router(ratings.router)









