Instalily Case Study – Conversational Appliance Support Agent

Author: Kosta Karathanasopoulos
Date: November 2025

⸻

1. Project Goals

Design a scoped, reliable chat assistant for the PartSelect website that:
	•	Helps users find refrigerator and dishwasher parts
	•	Checks compatibility with appliance model numbers
	•	Provides step-by-step installation instructions
	•	Troubleshoots common appliance symptoms
	•	Rejects all out-of-domain questions
	•	Integrates with the Deepseek LLM for reasoning and explanation
	•	Uses a vector database + metadata grounding to prevent hallucinations
	•	Produces structured responses for a clean, product-focused UI
	•	Maintains an extensible, scalable architecture for future appliances and features

⸻

2. High-Level System Architecture

┌──────────────────────────────┐
│           React UI           │
│   - Chat Window              │
│   - Product Cards            │
│   - Quick Action Buttons     │
└───────────────▲──────────────┘
│ POST /chat
┌───────────────┴──────────────┐
│         Backend API           │
│  (Node.js / Python FastAPI)   │
│                               │
│  - chat router                │
│  - intent classification      │
│  - tool execution layer       │
│  - retrieval orchestration    │
└───────────────▲──────────────┘
│ vector search
┌───────────────┴──────────────┐
│       Vector Database         │
│   (Pinecone / Supabase)       │
│   - Part embeddings           │
│   - Compatibility metadata    │
│   - Installation text         │
└───────────────▲──────────────┘
│ grounding
┌───────────────┴──────────────┐
│         Deepseek LLM          │
│   - intent classification      │
│   - explanation synthesis      │
│   - troubleshooting reasoning │
│   - structured JSON output    │
└──────────────────────────────┘

⸻

3. Core Features & System Behavior

3.1 Strict Domain Guardrails

The assistant must only answer questions about:
	•	Refrigerators
	•	Dishwashers
	•	OEM appliance parts
	•	Installation instructions
	•	Troubleshooting symptoms
	•	Model compatibility

Everything else must be refused with a friendly, scoped message.

⸻

3.2 Agent Workflow
	1.	Intent Classification
Deepseek determines whether the user wants installation help, compatibility checking, troubleshooting, product lookup, or is out of scope.
	2.	Retrieval
The agent queries a vector DB for relevant product entries and metadata.
	3.	Tool Execution
Depending on intent, call the appropriate internal tool:
	•	search_parts
	•	check_compatibility
	•	get_install_steps
	•	troubleshoot_symptoms
	4.	Deepseek Synthesis
Deepseek reorganizes the retrieved data, explains it clearly, and returns structured JSON.
	5.	Frontend Rendering
The UI displays product cards, installation steps, warnings, and compatibility results.

⸻

4. Data Model

Example Part Record:

{
“part_number”: “PS11752778”,
“name”: “Refrigerator Ice Maker Assembly”,
“type”: “refrigerator”,
“compatible_models”: [“WDT780SAEM1”, “ED5FHEXVB00”],
“symptoms_fixed”: [
“ice maker not working”,
“no water dispensing”,
“ice not ejecting”
],
“install_instructions”: “1. Unplug refrigerator…\n2. Remove ice bin…\n3. etc.”,
“description”: “OEM Whirlpool ice maker assembly designed for modern refrigerators.”,
“price”: 89.99,
“image_url”: “https://example.com/ps11752778.jpg”,
“product_url”: “https://www.partselect.com/PS11752778”
}

Approximately 20–40 part entries are sufficient for the case study.

⸻

5. API Design

POST /chat
Request:
{
“message”: “How do I install PS11752778?”,
“conversation_id”: “123”
}

Response:
{
“type”: “installation”,
“steps”: [“Unplug the refrigerator…”, “Remove the ice bin…”],
“product”: { “part_number”: “PS11752778”, “price”: 89.99, “image_url”: “…” }
}

⸻

6. Backend File Structure

backend/
routes/
chat.js
services/
deepseek.js
vectorSearch.js
toolExecutor.js
data/
seedParts.json
utils/
formatters.js

⸻

7. Frontend Architecture (React)

src/
components/
ChatWindow.jsx
MessageBubble.jsx
ProductCard.jsx
QuickActions.jsx
pages/
ChatPage.jsx
api/
chat.js
styles/
chat.css

ProductCard displays:
	•	Product image
	•	Part name
	•	Price
	•	Compatibility badges
	•	Link to PartSelect product page
	•	Button for installation steps

⸻

8. Extensibility

The system can easily expand to:

Additional appliances
	•	Washer
	•	Dryer
	•	Oven
(Just add new part data + embeddings)

Additional features
	•	Order lookup
	•	Returns & warranty
	•	OCR model number detection
	•	Image troubleshooting
	•	Add-to-cart integration
	•	Multi-agent routing
	•	Support for more product categories

The architecture does not need to be rebuilt — only extended.

⸻

9. Deployment Considerations
	•	Deploy React frontend to Vercel or Netlify
	•	Deploy backend to Render, Railway, or AWS
	•	Use environment variables for Deepseek & DB keys
	•	CORS limited to PartSelect domains
	•	Rate limiting to prevent LLM abuse
	•	Pinecone / Supabase for embeddings

⸻

10. Summary

This architecture:
	•	Stays tightly scoped to refrigerators and dishwashers
	•	Prevents hallucinations via retrieval instead of LLM guessing
	•	Uses Deepseek strictly for reasoning and formatting
	•	Produces structured, UI-friendly responses
	•	Scales smoothly as product lines and features expand
	•	Meets all success criteria defined in the case study
