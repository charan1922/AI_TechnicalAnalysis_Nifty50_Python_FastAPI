from app.routers.threads import router as threads_router
from app.routers.message import router as messages_router
from app.routers.response_api.response import router as response_api_router
from app.routers.response_api.sessions import router as sessions_router

all_routes = [threads_router, messages_router, response_api_router, sessions_router]
