# Sellince-agent
Turning passive mobile apps into revenue engines. AI sales agent that knows when to reach out and what to offer.
# Sellince Agent Backend API

## System Overview
This repository contains the backend infrastructure for the Sellince Agent, a state-aware AI telecom sales assistant. The system is built using FastAPI for the web server routing and LangGraph for the underlying AI state machine. 

This backend is designed to operate completely independent of the frontend, processing user input, managing session memory, and returning strict JSON contracts that dictate both conversational text and frontend UI actions.

### Core Capabilities
* **State Machine Routing:** The agent moves through predefined conversational stages (Engage, Explain, Close) using LangGraph. It evaluates customer intent at every node to determine the appropriate response strategy.
* **Bilingual Support:** The AI automatically detects the user's language (English or Arabic, including regional Levantine dialects) and responds in the matching language and tone. Hardcoded keyword detection matrices have been updated to support bilingual triggers.
* **Dynamic Action Payloads:** When the AI determines the customer has reached a purchasing decision, the state machine intercepts the standard chat response and generates an `action_payload`. This payload commands the frontend to render specific UI elements, such as a checkout button dynamically routed to the correct product ID.
* **Session Management:** Conversation history is tracked via a `customer_id`. The backend handles memory retention and applies aggressive context-wiping when topics shift, preventing AI hallucinations or context bleed.
* **Safety Guardrails:** Hardcoded filters intercept abusive language or out-of-scope requests before they reach the LLM, returning professional fallback responses.

---

## Local Setup and Installation

To ensure the backend runs correctly on your local machine, you must configure a virtual environment and supply your own API keys. 

### 1. Environment Preparation
Open your terminal and navigate to the project directory:

```bash
cd backend
```

Create a Python virtual environment to isolate the dependencies:

```bash
# For Windows
python -m venv venv
.\venv\Scripts\activate

# For Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
Install the required packages from the requirements file:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Because security practices dictate that API keys are never pushed to version control, you must create a local environment file.

Create a new file named `.env` in the root of the `backend/` directory and add your Groq API key:

```text
GROQ_API_KEY=your_api_key_here
```

### 4. Run the Server
Start the FastAPI server using Uvicorn:

```bash
uvicorn app.main:app --reload
```
The server will start running on `http://127.0.0.1:8000`.

---

## Testing the Integration

### Swagger UI
Once the server is running, the easiest way to test the integration is via the auto-generated Swagger documentation. 
1. Navigate your browser to: `http://127.0.0.1:8000/docs`
2. Open the `POST /api/chat` route and click "Try it out".

### API Contract Example
The frontend should interact with the backend using the following JSON structure.

**Request:**
```json
{
  "customer_id": 14,
  "message": "I want the fiber bundle, let's do it"
}
```

**Response:**
```json
{
  "response": "Excellent choice. I have prepared your fiber bundle setup.",
  "action_payload": {
    "label": "Continue to Purchase",
    "url": "/checkout?customer_id=14&agent_id=45&product_id=fiber_bundle"
  },
  "sales_stage": "close"
}
```
*Note for Frontend Developers: If `action_payload` returns as `null`, render the text normally without UI buttons.*

### Automated Tests
To run the end-to-end integration suite and verify the API contract is intact, open a second terminal (with the virtual environment activated) and run:

```bash
python run_tests.py
```