from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

from core import routes

from core.database import Base, engine
from core import models

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,           
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router, prefix="/api")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created.")

if __name__ == "__main__":
    # Get the port from the environment variable
    port = int(os.environ.get("PORT", 8000))  # Default to 8000 for local development
    # Run the application with Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)