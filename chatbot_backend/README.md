# The LuxeProject

## Overview

This project is a multi-agent AI system designed to act as an intelligent e-commerce assistant. Built on a modular, tool-based architecture, it automates core customer service functions by leveraging Retrieval-Augmented Generation (RAG) for personalized, data-driven responses and integrates with a no-code automation platform for real-world actions like managing returns.

The system is engineered for reliability and scalability, encapsulating all components within a Docker container for consistent deployment across different environments.

---

## Features

* **Multi-Agent System**: A hierarchy of specialized agents, each with a distinct role, to handle a variety of customer inquiries.
* **Intelligent Routing**: A RouterAgent that intelligently directs user queries to the most appropriate downstream agent.
* **Tool-Augmented Capabilities**: Agents are equipped with custom tools to perform specific, real-world tasks, such as tracking orders, initiating returns, and providing product information.
* **Context-Aware Responses (RAG Pipeline)**: Utilizes a vector database to provide accurate and grounded answers based on a dedicated knowledge base of product FAQs and information.
* **No-Code Automation Integration**: The ReturnsAgent is integrated with an n8n webhook to trigger an automated workflow, demonstrating a seamless connection between AI and no-code platforms.
* **Containerized Environment**: The entire application is containerized with Docker, ensuring easy setup, portability, and deployment to any cloud service.

---

## System Architecture

The system follows a modular, three-tier architecture that separates concerns for clarity and maintainability.

1. **AI Agents Layer**: Specialized AI agents (RouterAgent, CustomerServiceAgent, OrderTrackingAgent, ReturnsAgent, StyleAdvisorAgent, ProductInfoAgent). They are the primary interface for processing user queries.
2. **Tools & API Layer**: Houses the tools that enable the agents to perform actions. The `api_client.py` serves as the central hub for all external API communications.
3. **Knowledge & Automation Layer**: Includes the RAG pipeline (`vector_store.py`, `vector_db_tool.py`) for data retrieval and the external no-code automation platform (n8n) for executing workflows.

---

## Core Components

### AI Agents

* **RouterAgent**: Entry point of the system. Routes queries to specialized agents.
  *Goal*: Route user queries correctly.

* **CustomerServiceAgent**: Handles general product information, troubleshooting, and FAQs using RAG.
  *Goal*: Provide accurate answers to customer queries.

* **OrderTrackingAgent**: Provides real-time updates on orders.
  *Goal*: Retrieve and interpret shipping/order data.
  *Tools*: `OrderTrackingTool`.

* **StyleAdvisorAgent**: Provides personalized product recommendations.
  *Goal*: Suggest products tailored to preferences.
  *Tools*: `StyleAdvisorTool`.

* **ReturnsAgent**: Manages returns and exchanges with external workflow automation.
  *Goal*: Automate and streamline return requests.
  *Tools*: `ReturnsTool`.

* **ProductInfoAgent**: Answers detailed product-specific queries.
  *Goal*: Provide product details (dimensions, materials, etc.).
  *Tools*: `ProductInfoTool`.

### RAG Pipeline

* **vector\_store.py**: Handles ingestion/storage of the knowledge base, embedding generation, and vector database storage.
* **vector\_db\_tool.py**: Provides semantic search functionality for retrieving relevant information.

### Intelligent Automation

* **n8n Workflow**: A webhook that accepts return requests from the ReturnsAgent. Can trigger email confirmations, update Google Sheets, or perform other return-related workflows.

---

## Getting Started

### Prerequisites

* Docker installed on your machine.
* A `.env` file with the necessary API keys for your LLM and vector database.
* An **n8n** instance or webhook URL configured to accept POST requests.

### Setup

```bash
# Clone the Repository
git clone https://github.com/Ermias289/E-Commerce.git
cd E-Commerce

# Configure Environment Variables
# Create a .env file in the root directory with:
GOOGLE_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
N8N_WEBHOOK_URL=your_n8n_webhook_url
# Add other necessary keys for your vector DB, etc.

# Build and Run with Docker
docker build -t e-commerce-assistant .
docker run -it --env-file .env e-commerce-assistant
```

This builds the Docker image, uses your `.env` for environment variables, and starts the app.

---

## Deployment

The Dockerized application can be deployed to **Render, AWS, Google Cloud**, or any container service. Push the image to Docker Hub (or another registry) and configure your cloud platform to pull and run it.

---

## Future Enhancements

* **Dynamic Product Catalog**: Integrate with a live product database for real-time stock and price info.
* **Customer Authentication**: Add login/auth features to personalize order history and recommendations.
* **Live Chat Integration**: Connect the AI system to a chat service (Slack, Intercom, etc.) for real-time conversation.

---

