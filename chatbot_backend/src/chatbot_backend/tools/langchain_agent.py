import os
from dotenv import load_dotenv
from typing import List
import sys
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.tools import BaseTool

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, project_root)

from src.chatbot_backend.tools.vector_db_tool import VectorDBTool

# Load environment variables
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

def create_agent() -> AgentExecutor:
    """
    Creates and returns a LangChain agent executor configured to answer
    questions using a vector database tool.
    """
    #  Defining the tools the agent can use
    tools: List[BaseTool] = [VectorDBTool()]

    #  Defining the LLM
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY")
    )

    #  Creating the agent prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", 
             "You are a helpful and polite customer service AI for an e-commerce store named 'ChronoCraft'. "
             "Your main task is to answer user questions about products and frequently asked questions (FAQs). "
             "Use the 'vector_db_query' tool to find relevant information. "
             "If the user asks about a topic outside of products or FAQs, politely state that you can't help with that specific request. "
             "Do not make up information. Use only the information provided by the tool. "
             "Your tone should be friendly and professional."),
            
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    # Creating the agent
    agent = create_tool_calling_agent(llm, tools, prompt)

    # Creating the agent executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor

if __name__ == "__main__":
    agent_executor = create_agent()
    
    print("Agent is ready. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        
        try:
            # Invoke the agent with the user's input
            response = agent_executor.invoke({"input": user_input, "chat_history": []})
            print(f"AI: {response['output']}\n")
        except Exception as e:
            print(f"AI: I'm sorry, an error occurred. {e}")