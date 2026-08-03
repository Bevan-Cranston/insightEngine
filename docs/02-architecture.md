# Architecture

Insight Engine is designed to provide a conversational AI experience that retains useful context across long periods and multiple interactions.
The system connects a mobile-accessible web interface to an LLM model for reasoning and database for persistent message storage.
Product value is being built around a system of retrieval for messages that relate to the current message for prompt injection.
This RAG system uses traditional embedding techniques to match based on semantic similarity, but will be extended to a hybrid system 
using a custom tag extraction and matching system.

                    User
                      │
                      ▼
         Mobile Web Interface
                (HTML/JS)
                      │
                      ▼
                 FastAPI API
                      │
                      ▼
           Retrieval Layer (RAG)
              ┌────────┴────────┐
              ▼                 ▼
         OpenAI API         MongoDB
        (Reasoning)      (Persistence)

