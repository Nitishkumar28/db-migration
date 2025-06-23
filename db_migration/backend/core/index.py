from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import routes

from core.database import Base, engine
from core import models

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router, prefix="/api")

Base.metadata.create_all(bind=engine)
print("✅ Tables created.")