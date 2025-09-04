from fastapi import APIRouter, status
from pydantic import BaseModel
from typing import Dict

router = APIRouter(tags=["Chatbot"])

class ChatRequest(BaseModel):
    message: str

@router.get("/health", status_code=status.HTTP_200_OK, response_model=Dict[str, str])
def health_check():
    """
    Performs a health check on the chatbot API.
    """
    return {"status": "ok"}

@router.post("/query", status_code=status.HTTP_200_OK, response_model=Dict[str, str])
def chat_query(request: ChatRequest):
    """
    Processes a user query and returns a response from the GenAI agent.
    
    NOTE: This endpoint is currently a placeholder and will be connected to
    the LangChain/CrewAI agent in the next milestone.
    """
    return {"response": f"Received your query: {request.message}. Processing... (Milestone 2 will add the agent logic)"}