from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Initialize the FastAPI app
app = FastAPI(
    title="E-Commerce AI Chatbot",
    description="Welcome to our AI-powered customer service chatbot! 🤖",
    version="1.0.0"
)

class ChatRequest(BaseModel):
    """
    A Pydantic model for the incoming chat request body.
    """
    text: str

@app.get("/", status_code=200)
def welcome():
    """
    Friendly welcome message for the root endpoint.
    """
    return {
        "message": "🎉 Welcome to the E-Commerce AI Chatbot API!",
        "description": "Your intelligent shopping assistant is ready to help with orders, product searches, and customer support.",
        "status": "ready to chat! 💬"
    }

@app.get("/health", status_code=200, tags=["healthcheck"])
def health_check():
    """
    Endpoint to check the health of the API.
    Returns a simple JSON response to indicate the service is running.
    """
    return {"status": "healthy", "message": "Chatbot API is up and running! ✅"}

@app.post("/chat", status_code=200, tags=["chatbot"])
def chat(request: ChatRequest):
    """
    Simple chatbot endpoint with a friendly response.
    This will be enhanced in future iterations.
    """
    return {
        "response": f"Hello! I received your message: '{request.text}' 😊",
        "message": "I'm your AI shopping assistant! I'll be getting smarter soon to help you with orders, product searches, and more!",
        "status": "message received"
    }


if __name__ == "__main__":
    uvicorn.run(
        "chatbot_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )