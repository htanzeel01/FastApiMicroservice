import uvicorn
from app import create_app  # Import create_app from your app structure

# Create the FastAPI app
app = create_app()

# If this script is run directly (not inside Docker), uvicorn will run the app
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
