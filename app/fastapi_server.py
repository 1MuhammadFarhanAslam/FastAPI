# Import the necessary modules
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Define the function to create the FastAPI application
def create_app():
    # Set the project root path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # Add the project root directory to the Python path
    sys.path.insert(0, project_root)

    # Import routers from the 'routers' package using relative imports
    from routers import admin, user, login

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
