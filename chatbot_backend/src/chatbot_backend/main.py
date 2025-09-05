from fastapi import FastAPI
from ..chatbot_api import router as chatbot_router

# Initialize the FastAPI application
app = FastAPI(
    title="Luxe GenAI System",
    description="A generative AI system for home decor e-commerce.",
    version="0.1.0",
)

# Include the chatbot API router
app.include_router(chatbot_router, prefix="/chatbot")

@app.get("/", tags=["Root"])
def read_root():
    """
    Root endpoint for the API.
    """
    return {"message": "Welcome to the Luxe GenAI System API. Navigate to /docs for API documentation."}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)