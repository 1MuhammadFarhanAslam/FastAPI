import asyncio
from fastapi import FastAPI
from routers import admin, user, login
from fastapi.middleware.cors import CORSMiddleware

# Define a function to create the FastAPI application
def create_app():
    # Create FastAPI application object
    app = FastAPI()

    # Allow CORS for all domains in this example
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(login.router, prefix="", tags=["Authentication"])
    app.include_router(admin.router, prefix="", tags=["Admin"])
    app.include_router(user.router, prefix="", tags=["User"])

    return app

# Call create_app() to obtain the FastAPI application instance
app = create_app()
