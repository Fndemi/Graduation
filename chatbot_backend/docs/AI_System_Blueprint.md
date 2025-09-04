# AI System Blueprint

This blueprint outlines the full AI system architecture for the e‑commerce chatbot, showing the flow of a user's request from the frontend to the final response, integrating all required components.

---

## 1) AI System Architecture Diagram

### 1.1 Conceptual Flow (Mermaid)

```mermaid
flowchart LR
    U[User on Web/Mobile UI] -->|Types query| FE[Frontend]
    FE -->|REST/JSON POST /chat| API[FastAPI Backend]
    API -->|Intent + Complexity Routing| RT{Router}

    RT -->|Simple/FAQ/Product Qs| LC[LangChain Agent]
    RT -->|Complex Multi-Step (e.g., WISMO)| CR[CrewAI Orchestrator]

    subgraph Agents
      LC --calls--> T[MCP Tools Layer]
      CR --delegates--> A1[OrderTrackingAgent]
      CR --delegates--> A2[CustomerServiceAgent]
      CR --delegates--> A3[ReturnsAgent]
      A1 --calls--> T
      A3 --calls--> T
    end

    subgraph Tools (MCP)
      T --> PS[(ProductSearchTool)]
      T --> OT[(OrderTrackingTool)]
      T --> AC[(AddToCartTool)]
      T --> IR[(InitiateReturnTool)]
    end

    subgraph External Services
      PS --> VDB[(Vector DB / RAG embeddings)]
      OT --> ECOM[(E‑commerce API)]
      ECOM --> SHIP[(3rd‑party Shipping API)]
      AC --> ECOM
      IR --> N8N[(n8n Workflow)]
    end

    LC -->|Response JSON| API
    CR -->|Final message JSON| API
    API --> FE -->|Rendered chat + rich cards| U
```

### 1.2 Alternate ASCII Diagram

```
User → Frontend(UI) → FastAPI(/chat)
                  ↘ Router ↙
     ┌─────────────┴─────────────┐
     │                           │
LangChain Agent            CrewAI Orchestrator
   │  │                        │   │   │
   │  └─(MCP Tools)────────────┘   │   └─► ReturnsAgent ──(InitiateReturnTool)──► n8n
   │                                └─► CustomerServiceAgent (no external tools)
   └─► ProductSearchTool ─► Vector DB
       AddToCartTool ─────► E‑commerce API
       OrderTrackingTool ─► E‑commerce API ─► Shipping API
```

---

## 2) CrewAI Agent Roles & Responsibilities

### 2.1 OrderTrackingAgent

* **Responsibility:** Logistics expert; finds and interprets shipping info.
* **Primary Task:** `Find the current status of order [order_number].`
* **Tool Usage:** Exclusively uses `get_order_status` (OrderTrackingTool).
* **Inputs:** `order_number`, optional `user_id` for permission checks.
* **Outputs:** Normalized `order_status_data` (carrier, last\_update, ETA, events\[]).

### 2.2 CustomerServiceAgent

* **Responsibility:** Communication expert; formats friendly, brand‑aligned replies.
* **Primary Task:** `Format the [order_status_data] into a clear and friendly message for the user.`
* **Tool Usage:** None (pure reasoning + templating).
* **Inputs:** `order_status_data`, conversation context, tone/style guide.
* **Outputs:** Final message with optional UI hints (e.g., status badge, timeline).

### 2.3 ReturnsAgent

* **Responsibility:** Returns specialist; initiates returns and manages logistics.
* **Primary Task:** `Initiate a return for order [order_number] and generate a return label.`
* **Tool Usage:** Uses `initiate_return` (InitiateReturnTool → triggers n8n).
* **Inputs:** `order_id`, line items to return, reason codes, pickup/label preference.
* **Outputs:** Return RMA id, label/link, next steps for the user.

---

## 3) MCP (Model Context Protocol) Tool Architecture

The MCP layer standardizes how agents call backend functions. Each tool exposes a clear, typed interface that maps directly to FastAPI endpoints.

### 3.1 ProductSearchTool

* **Description:** Searches the product database for items that match the user's query via semantic similarity.
* **Function Signature (Agent‑side):** `def search_products(query: str, top_k: int = 8) -> List[Dict]`
* **Backend Call (FastAPI):** `POST /tools/product_search` → queries Vector DB (FAISS/Pinecone/Weaviate) with text/image embeddings.
* **Return Shape:**

```json
{
  "results": [
    {"product_id": "p123", "title": "Black Sneakers", "score": 0.84,
     "price": 5999, "currency": "KES", "image": "https://...", "url": "/product/p123"}
  ]
}
```

### 3.2 OrderTrackingTool

* **Description:** Retrieves real‑time shipping status for a given order number.
* **Function Signature (Agent‑side):** `def get_order_status(order_number: str) -> Dict`
* **Backend Call (FastAPI):** `GET /tools/order_status/{order_number}` → calls E‑commerce API `/api/orders/{order_number}/status` → may query carrier API.
* **Return Shape:**

```json
{
  "order_number": "A10045",
  "carrier": "DHL",
  "status": "In Transit",
  "eta": "2025-09-06",
  "last_update": "2025-09-03T12:30:00Z",
  "events": [
    {"time": "2025-09-02T08:00:00Z", "location": "Nairobi HUB", "description": "Departed facility"}
  ]
}
```

### 3.3 AddToCartTool

* **Description:** Adds a specific product to the user's shopping cart.
* **Function Signature (Agent‑side):** `def add_to_cart(product_id: str, quantity: int, user_id: str) -> str`
* **Backend Call (FastAPI):** `POST /tools/add_to_cart` → forwards to E‑commerce API `/api/cart/add`.
* **Return Shape:** `{ "message": "Added to cart", "cart_id": "c789", "line_item_id": "li222" }`

### 3.4 InitiateReturnTool

* **Description:** Starts a return process and sends confirmation email via n8n.
* **Function Signature (Agent‑side):** `def initiate_return(order_id: str, items: List[Dict], reason: str) -> str`
* **Backend Call (FastAPI):** `POST /tools/initiate_return` → triggers n8n webhook (automation for RMA + email).
* **Return Shape:** `{ "rma_id": "RMA-5542", "label_url": "https://.../label.pdf" }`

---

## 4) FastAPI Contracts (for Frontend & Tools)

### 4.1 Chat Inference Endpoint (Frontend → FastAPI)

* **Path:** `POST /chat`
* **Request:**

```json
{
  "user_id": "u123",
  "message": "Where is my order A10045?",
  "attachments": [],
  "session_id": "s456",
  "ui_capabilities": {"supports_cards": true, "supports_buttons": true}
}
```

* **Behavior:**

  * Router computes intent & complexity (e.g., via lightweight classifier or prompt‑based decision).
  * Routes to LangChain Agent (simple) or CrewAI Orchestrator (complex).
* **Response (unified):**

```json
{
  "type": "chat_message",
  "text": "Your order A10045 is in transit with DHL. ETA: Sep 6.",
  "rich": {
    "status_badge": "in_transit",
    "timeline": [
      {"time": "2025-09-02T08:00:00Z", "label": "Departed Nairobi HUB"}
    ]
  },
  "suggested_replies": ["Track another order", "Return an item"],
  "source": "CrewAI"
}
```

### 4.2 Tool Endpoints (Agents → FastAPI)

* `POST /tools/product_search { query, top_k }`
* `GET /tools/order_status/{order_number}`
* `POST /tools/add_to_cart { user_id, product_id, quantity }`
* `POST /tools/initiate_return { order_id, items[], reason }`

> **Auth:** All tool routes require service auth (e.g., JWT with service role) + user scoping where needed.

---

## 5) RAG & Embeddings Layer (for ProductSearchTool)

* **Embeddings:** Use text (title, description, category, attributes) and optional image embeddings (CLIP) → store in Vector DB with metadata.
* **Schema Example:**

```json
{
  "id": "p123",
  "embedding": [ ... ],
  "metadata": {
    "title": "Black Sneakers",
    "price": 5999,
    "currency": "KES",
    "brand": "Acme",
    "category": "Shoes",
    "image": "https://...",
    "url": "/product/p123"
  }
}
```

* **Retrieval:** Hybrid search (keyword + vector). Top‑k results passed to LLM as context for conversational answers or product carousels.

---

## 6) Orchestration Logic

### 6.1 Routing Heuristics

* **Simple/LangChain:** FAQs, store policies, generic product discovery, sizing guidance.
* **Complex/CrewAI:** WISMO (Where Is My Order), returns/exchanges, multi‑step flows (verify user → fetch status → format response).

### 6.2 CrewAI Playbooks

* **Order Tracking Playbook:**

  1. OrderTrackingAgent → `get_order_status` with `order_number`.
  2. CustomerServiceAgent → format `order_status_data` with tone guide.
* **Returns Playbook:**

  1. ReturnsAgent → `initiate_return` with selected items & reason.
  2. CustomerServiceAgent → confirm RMA, label, and next steps.

---

## 7) Security & Compliance

* **AuthN/Z:**

  * Frontend → FastAPI: user JWT (issued by your auth provider).
  * Agents → Tool routes: service JWT + RBAC; verify `user_id` scope where needed.
* **PII Handling:** Minimize in prompts; mask email/phone; never log raw PII.
* **Secrets:** Store API keys in vault/ENV (`ECOM_API_KEY`, `VDB_URL`, `N8N_WEBHOOK_URL`).
* **Rate Limiting:** Per user/session and per tool to prevent abuse.

---

## 8) Observability & Evaluation

* **Tracing:** Use OpenTelemetry to trace request → router → agents → tools → externals.
* **Structured Logs:** Include `session_id`, `user_id`, latency per tool call, token usage.
* **Quality:** Log user feedback thumbs‑up/down; maintain eval dataset for regression tests.

---

## 9) Error Handling Patterns

* **Tool Failures:** Return graceful fallbacks ("We’re having trouble contacting the carrier"), suggest human handoff.
* **Timeouts/Backoffs:** Exponential backoff on external APIs; circuit breaker for carriers.
* **Validation:** Strict request schemas; sanitize tool inputs.

---

## 10) Example Prompts (Summarized)

* **LangChain System Prompt:**

  * Role: Helpful e‑commerce assistant.
  * Tools: product\_search, add\_to\_cart, order\_status, initiate\_return (when routed to Crew).
  * Style: Friendly, concise, localized currency (KES).
* **CustomerServiceAgent Style Guide:**

  * Voice: Warm, helpful, specific; avoid generic filler; include concrete dates.

---

## 11) Deployment Topology

* **Services:** FastAPI (ASGI) + Workers for tool calls; Vector DB managed (Pinecone/Weaviate); n8n hosted; E‑commerce API by web team.
* **Scaling:** Autoscale FastAPI; cache hot product results; CDN for images.

---

## 12) Handover Checklist (for Frontend Team)

* `/chat` contract + sample payloads/responses.
* Rich UI hints (cards, badges, timelines, suggested replies).
* Error states and retry guidance.
* Authentication expectations and headers.

---

## 13) Next Steps

1. Stand up FastAPI skeleton with `/chat` + tool routes.
2. Integrate vector DB + embeddings pipeline for products.
3. Implement routing + LangChain agent.
4. Add CrewAI crew (OrderTracking, CustomerService, Returns) and wire the MCP tools.
5. Ship observability + eval harness.

> This document is ready to share with your teammates as the authoritative spec for the AI layer.
