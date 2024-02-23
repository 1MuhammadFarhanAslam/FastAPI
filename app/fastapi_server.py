# Import the necessary modules
from getpass import getpass  # Use getpass to hide the password input
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from .admin_database import get_database, verify_hash, Admin
from typing import Optional, Union
import os
import sys

# Define the function to create the FastAPI application
def create_app(secret_key: str):
    # Set the project root path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # Add the project root directory to the Python path
    sys.path.insert(0, project_root)

    # Import routers from the 'routers' package using relative imports
    from .routers import admin, user, login

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

    # Basic HTTP authentication
    security = HTTPBasic()

    # Define the function to authenticate admins
    def authenticate_admin(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_database)):
        # Prompt for username and password
        username = input("Enter admin username: ")
        password = getpass("Enter admin password: ")

        # Check if the credentials match the provided username and password
        if not (username == credentials.username and password == credentials.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Basic"},
            )
        return credentials.username

    # Include routers
    app.include_router(login.router, prefix="", tags=["Authentication"])
    app.include_router(admin.router, prefix="", tags=["Admin"], dependencies=[Depends(authenticate_admin)])
    app.include_router(user.router, prefix="", tags=["User"])

    return app

# Prompt for secret key before running the application
secret_key = input("Enter secret key: ")

# Call create_app() to obtain the FastAPI application instance
app = create_app(secret_key)
