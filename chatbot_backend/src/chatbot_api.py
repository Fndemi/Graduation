from fastapi import APIRouter, status
from pydantic import BaseModel
from typing import Dict
from crewai import Agent, Task, Crew, Process
from crewai import LLM
import os
from dotenv import load_dotenv
import yaml
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from src.chatbot_backend.tools.custom_tool import OrderTrackingTool, StyleAdvisorTool, ReturnsTool, VectorDBTool

# Initialize FastAPI router
router = APIRouter(tags=["Chatbot"])

# Load Environment Variables & LLM Configuration
load_dotenv()
os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY")

gemini_llm = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=os.environ["GEMINI_API_KEY"]
)

# Initialize Custom Tools
def initialize_tools():
    TOOLS = {}
    try:
        TOOLS["OrderTrackingTool"] = OrderTrackingTool()
        TOOLS["ReturnsTool"] = ReturnsTool()
        TOOLS["StyleAdvisorTool"] = StyleAdvisorTool()
        TOOLS["ProductInfoTool"] = VectorDBTool() 
    except Exception as e:
        print(f"❌ Failed to initialize a tool: {e}")
    return TOOLS

TOOLS = initialize_tools()

# Corrected Utility Functions
def load_yaml_config(filepath):
    """Loads configuration from a YAML file from a reliable path."""
    abs_path = os.path.join(
        os.getcwd(),
        "src",
        "chatbot_backend",
        "config",
        filepath
    )
    
    try:
        with open(abs_path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"⚠️ Error: The configuration file '{abs_path}' was not found.")
        return {}

def create_agent_and_task(agents_config, tasks_config, agent_key, task_key, query, tools_dict):
    agent_config = agents_config.get(agent_key)
    task_config = tasks_config.get(task_key)

    if not agent_config or not task_config:
        print(f"⚠️ Error: Configuration not found for {agent_key} or {task_key}.")
        return None, None
    
    agent_tools = [
        tools_dict[tool_name] 
        for tool_name in agent_config.get("tools", []) 
        if tool_name in tools_dict
    ]
    
    specialized_agent = Agent(
        role=agent_config["role"],
        goal=agent_config["goal"],
        backstory=agent_config["backstory"],
        tools=agent_tools,
        llm=gemini_llm,
        verbose=True
    )
    specialized_task = Task(
        description=f"{task_config['description']}. Customer query: '{query}'",
        expected_output=task_config["expected_output"],
        agent=specialized_agent
    )
    return specialized_agent, specialized_task

# Main CrewAI processing function
def run_crew_for_query(query: str):
    router_agent = Agent(
        role="Customer Service Router",
        goal="Analyze the user's request and route it.",
        backstory="You are the first point of contact.",
        llm=gemini_llm,
        verbose=True
    )
    router_task = Task(
        description=f"Analyze the following customer query: '{query}'. Your final answer must be a single word from this list: 'track', 'style', 'return', or 'info'. Do not include any other text or explanation.",
        expected_output="A single word from the list 'track', 'style', 'return', or 'info' that best categorizes the customer's intent.",
        agent=router_agent
    )
    
    router_crew = Crew(agents=[router_agent], tasks=[router_task], process=Process.sequential)
    router_result = router_crew.kickoff()
    final_output_text = str(router_result).strip().lower()

    agents_config = load_yaml_config("agents.yaml")
    tasks_config = load_yaml_config("tasks.yaml")

    agent, task = None, None
    if final_output_text == "track":
        agent, task = create_agent_and_task(agents_config, tasks_config, "order_tracking_agent", "track_order_task", query, TOOLS)
    elif final_output_text == "return":
        agent, task = create_agent_and_task(agents_config, tasks_config, "returns_agent", "return_process_task", query, TOOLS)
    elif final_output_text == "style":
        agent, task = create_agent_and_task(agents_config, tasks_config, "style_advisor_agent", "style_recommendation_task", query, TOOLS)
    elif final_output_text == "info":
        agent, task = create_agent_and_task(agents_config, tasks_config, "product_info_agent", "product_info_task", query, TOOLS)
    
    if agent and task:
        final_crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True)
        final_result = final_crew.kickoff()
        return final_result
    else:
        return "The router could not determine a specialized task for your query. Please try again with a different query."

class ChatRequest(BaseModel):
    message: str

@router.post("/query", status_code=status.HTTP_200_OK, response_model=Dict[str, str])
def chat_query(request: ChatRequest):
    try:
        crew_output = run_crew_for_query(request.message)
        
        # This check is now robust and doesn't require importing CrewOutput
        if hasattr(crew_output, 'raw'):
            response_text = crew_output.raw
        else:
            response_text = str(crew_output)
            
        return {"response": response_text}
        
    except Exception as e:
        print(f"❌ An error occurred while processing the query: {e}")
        return {"response": "An internal error occurred while processing your request. Please try again later."}

@router.get("/health", status_code=status.HTTP_200_OK, response_model=Dict[str, str])
def health_check():
    return {"status": "ok"}