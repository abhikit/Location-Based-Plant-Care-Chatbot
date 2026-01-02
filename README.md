# 🌱 Location-Based Plant Care Chatbot


🎯 Key Objectives Achieved
	•	✅ Strong Retrieval-Augmented Generation (RAG) enforcement
	•	✅ OpenAI used only as a reasoning & language layer
	•	✅ Location-aware contextualization (weather, air, environment)
	•	✅ Conversational memory support
	•	✅ Frontend–Backend decoupled architecture
	•	✅ Vision pipeline provisioned (image optional, non-mandatory)
	•	✅ No hallucinations, no fallback to generic LLM knowledge

⸻

🧠 Architectural Philosophy

LLMs are not a source of truth. They are a reasoning layer.

The system strictly follows this pipeline:

User Input (Text / Image / Location)
        ↓
Environment APIs (Weather, AQI, Climate)
        ↓
Vector Retrieval (Internal Knowledge Base)
        ↓
LLM (Reasoning + Language Only)
        ↓
Grounded, Context-Specific Plant Care Response

🚫 Hard Rule Enforced

No RAG → No Answer

If the retriever does not return relevant knowledge chunks, the system explicitly refuses to answer.

⸻

🔒 Hallucination Prevention Strategy

The LLM is constrained using:
	•	Explicit system prompts:
	•	“Answer using ONLY the provided plant knowledge”
	•	“If insufficient information exists, say so”
	•	Context isolation:
	•	Retrieved chunks = authoritative
	•	Conversation memory = supportive only
	•	Environment data = modifier, not knowledge
	•	Deterministic temperature settings

This ensures zero hallucination tolerance.

⸻

🧩 Core Capabilities in Phase-1

🌍 Location Awareness
	•	City ↔ Latitude/Longitude ↔ Map pin fully synchronized
	•	Environment parameters fetched dynamically:
	•	Temperature
	•	Humidity
	•	Rainfall
	•	Air quality indicators
	•	Environmental context explicitly reflected in answers

⸻

🧠 Strong RAG System
	•	Internal curated plant knowledge base
	•	Vector database for semantic retrieval
	•	Query-time grounding enforced
	•	No external plant knowledge leakage

⸻

🖼️ Vision-Ready (Optional Input)
	•	Image upload supported (non-mandatory)
	•	Text-only, image-only, and text+image flows handled
	•	Vision embeddings pipeline provisioned for Phase-2

⸻

💬 Conversational Memory
	•	Session-aware dialogue
	•	Past context influences phrasing, not facts
	•	Memory never overrides retrieved knowledge

⸻

🖥️ Frontend UX (Phase-1)
	•	Clean, map-based location selection
	•	Bi-directional sync:
	•	City → Map → Coordinates
	•	Map → City → Coordinates
	•	Environment cards displayed per location
	•	Non-blocking UI (optional text/image inputs)

⸻

🧪 Technology Stack

Layer	Tech
Frontend	HTML, CSS, JavaScript, Leaflet.js
Backend	FastAPI
Vector DB	ChromaDB
Embeddings	OpenAI embeddings
LLM	OpenAI (reasoning only)
Environment Data	Public weather & air APIs
Deployment-Ready	Local → AWS / Azure


⸻

🔐 Security & Responsibility
	•	No user PII stored
	•	No raw datasets sent to LLM
	•	Only retrieved snippets passed to OpenAI
	•	Designed for safe expansion into production environments

