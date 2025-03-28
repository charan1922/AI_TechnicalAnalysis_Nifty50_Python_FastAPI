from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.threads import router as threads_router
from app.routers.message import router as messages_router
from app.core.logger import configure_logging

# Configure logging
configure_logging()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Allows all origins. Replace with specific origins for better security.
    allow_credentials=True,  # Allows sending cookies from the frontend to the backend (if applicable)
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include the threads router
app.include_router(threads_router)
app.include_router(messages_router)

