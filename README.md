# Insight Engine

Insight Engine is a conversational AI system designed to retain and intelligently reuse context across long periods of 
interaction. Built with FastAPI, LangChain and MongoDB, the project explores hybrid retrieval, structured conversational 
memory and agentic context governance to support increasingly personalised LLM interactions.


Start the FastAPI development server from the project root:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Documentation

For further information, please see the growing engineering documentation set covering product direction,
system architecture, deployment and key design decisions.

- [Philosophy](docs/01-philosophy.md) — product vision and guiding philosophy
- [Architecture](docs/02-architecture.md) — current architecture and planned three-layer LLM design
- [Roadmap](docs/03-roadmap.md) — current state and future engineering work
- [Deployment](docs/04-deployment.md) — current deployment experiments and planned cloud architecture
- [Design Decisions](docs/design-decisions/) — architectural decision records (ADRs)
- [Investigations](docs/investigations/) — planned experiments around memory structuring and context governance

## Current State

The current MVP+ includes:

- Mobile HTML/CSS/JavaScript interface
- FastAPI application layer
- OpenAI LLM integration through LangChain
- MongoDB persistent conversation storage
- In-chat conversational memory
- Semantic retrieval across previous conversations
- Dockerized application layer

```text
Web Interface
     │
     ▼
   FastAPI
     │
  Retrieval
 ┌───┴────┐
 ▼        ▼
LLM    MongoDB
       
```