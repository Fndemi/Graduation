import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Dict
from src.chatbot_backend.tools.langchain_agent import create_agent
from langchain_core.messages import HumanMessage, AIMessage
from contextlib import asynccontextmanager
import uuid

# Import centralized logging
from logging_config import setup_logging

# Initialize logging system
loggers = setup_logging()
logger = loggers['main']
api_logger = loggers['api']

# Global variables
agent_executor = None
sessions: Dict[str, List] = {}

# Lifespan: Initialize and shutdown agent
@asynccontextmanager
async def lifespan(app: FastAPI):
    global agent_executor
    logger.info("Starting up: Initializing LangChain Agent...")
    try:
        agent_executor = create_agent()
        logger.info("Startup complete: Agent is ready to serve requests.")
    except Exception as e:
        logger.error(f"Failed to initialize agent: {e}", exc_info=True)
        raise
    yield
    logger.info("Shutting down: Application is closing.")

# FastAPI app
app = FastAPI(title="The Luxe", lifespan=lifespan)

# Pydantic models
class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

# Welcome endpoint
@app.get("/")
def welcome():
    api_logger.info("Welcome endpoint called")
    return {"message": "Welcome to The Luxe! How can I assist you today?"}

# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    api_logger.info(f"Received chat request: {request.query} (session_id={request.session_id})")
    try:
        # Get or create session
        session_id = request.session_id or str(uuid.uuid4())
        chat_history = sessions.get(session_id, [])

        # Invoke agent
        result = agent_executor.invoke({
            "input": request.query,
            "chat_history": chat_history
        })

        # Aggregate intermediate tool outputs + final agent output
        full_output = ""
        for step in result.get("intermediate_steps", []):
            # step = (tool, observation)
            tool_name, observation = step
            if observation:
                full_output += str(observation) + " "
        final_output = result.get("output", "")
        full_output += final_output
        full_output = full_output.strip()

        # Update session history
        chat_history.append(HumanMessage(content=request.query))
        chat_history.append(AIMessage(content=full_output))
        sessions[session_id] = chat_history[-10:]  # Keep last 10 messages

        api_logger.debug(f"Agent final output: {full_output}")
        return ChatResponse(response=full_output, session_id=session_id)

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}", exc_info=True)
        return ChatResponse(
            response="I'm sorry, I encountered an error. Please try again.",
            session_id=request.session_id or str(uuid.uuid4())
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
