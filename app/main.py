from fastapi import FastAPI
from app.database import Base, engine
from app.routers import schemes
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
# Allow requests from anywhere (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to ["http://localhost:8080"] if you want
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB tables
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(schemes.router)
