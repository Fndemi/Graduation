import os
import yaml
import argparse
import re
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai import LLM
# Import custom tools
from tools.custom_tool import OrderTrackingTool, StyleAdvisorTool, ReturnsTool, ProductInfoTool
from typing import List

#  Load Environment Variables & LLM Configuration ---
load_dotenv()

os.environ["GEMINI_API_KEY"] = os.getenv("GOOGLE_API_KEY")
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GOOGLE_API_KEY environment variable not set. Please set it in your .env file.")

gemini_llm = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=os.environ["GEMINI_API_KEY"]
)

#  Custom Tools
TOOLS = {
    "OrderTrackingTool": OrderTrackingTool(),
    "ReturnsTool": ReturnsTool(),
    "StyleAdvisorTool": StyleAdvisorTool(),
    "ProductInfoTool": ProductInfoTool(),
}

#  Utility Functions
def load_yaml_config(filepath):
    """Loads configuration from a YAML file."""
    abs_path = os.path.join(os.path.dirname(__file__), "config", filepath)
    try:
        with open(abs_path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"⚠️ Error: The configuration file '{abs_path}' was not found.")
        return {}

def create_agent_and_task(agents_config, tasks_config, agent_key, task_key, query):
    """Dynamically creates an agent and its corresponding task from config files."""
    agent_config = agents_config.get(agent_key)
    task_config = tasks_config.get(task_key)

    if not agent_config or not task_config:
        print(f"⚠️ Error: Configuration not found for {agent_key} or {task_key}.")
        return None, None
    
    agent_tools = [TOOLS[tool_name] for tool_name in agent_config.get("tools", []) if tool_name in TOOLS]

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

#  Main Execution Logic 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the CrewAI chatbot backend.")
    parser.add_argument("--query", type=str, required=True, help="The user query for the chatbot.")
    args = parser.parse_args()

    # Router agent
    router_agent = Agent(
        role="Customer Service Router",
        goal="Analyze the user's request and route it.",
        backstory="You are the first point of contact.",
        llm=gemini_llm,
        verbose=True
    )
    router_task = Task(
        description=f"Analyze the following customer query: '{args.query}'. Your final answer must be a single word from this list: 'track', 'style', 'return', or 'info'. Do not include any other text or explanation.",
        expected_output="A single word from the list 'track', 'style', 'return', or 'info' that best categorizes the customer's intent.",
        agent=router_agent
    )
    
    router_crew = Crew(agents=[router_agent], tasks=[router_task], process=Process.sequential)
    
    try:
        router_result = router_crew.kickoff()
        final_output_text = str(router_result).strip().lower()
        print(f"Router's decision: {final_output_text}")
    except Exception as e:
        print(f"❌ An error occurred during routing: {e}")
        exit()

    agents_config = load_yaml_config("agents.yaml")
    tasks_config = load_yaml_config("tasks.yaml")

    if final_output_text == "track":
        agent, task = create_agent_and_task(agents_config, tasks_config, "order_tracking_agent", "track_order_task", args.query)
    elif final_output_text == "return":
        agent, task = create_agent_and_task(agents_config, tasks_config, "returns_agent", "return_process_task", args.query)
    elif final_output_text == "style":
        agent, task = create_agent_and_task(agents_config, tasks_config, "style_advisor_agent", "style_recommendation_task", args.query)
    elif final_output_text == "info":
        agent, task = create_agent_and_task(agents_config, tasks_config, "product_info_agent", "product_info_task", args.query)
    else:
        print("⚠️ The router could not determine a specialized task.")
        exit()

    if agent and task:
        final_crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True)
        final_result = final_crew.kickoff()
        print("\n--- Final Results ---")
        print(final_result)