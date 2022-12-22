from typing import List
from fastapi import FastAPI, HTTPException
from core import db
from routers import routes


app = FastAPI()


db.register_db(app=app)
app.include_router(routes)
