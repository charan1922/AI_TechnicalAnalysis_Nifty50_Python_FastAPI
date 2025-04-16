from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import all_routes
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

# Include all routes
for route in all_routes:
    app.include_router(route)
