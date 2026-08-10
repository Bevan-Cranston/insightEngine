# Architecture

Insight Engine is designed to provide a conversational AI experience that retains useful context across long periods and 
multiple interactions. The system connects a mobile-accessible web interface to an LLM model for reasoning and database 
for persistent message storage. Product value is being built around a system of retrieval for messages that relate to 
the current message for prompt injection. This RAG system uses traditional embedding techniques to match based on 
semantic similarity, but will be extended to a hybrid system using a custom tag extraction and matching system.

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

Unlike traditional RAG systems that focus on embeddings / vectorized message representations, the tag extraction 
system will utilize an extra LLM reasoning pass to build keyword tags and other metadata for each stored message, 
such as:
- importance / future relevance
- recurring pattern
- breakthrough / unresolved friction
- suggested revisit timing

The system prompt for this LLM reasoning step will include a custom user profile that will be programmatically updated 
to allow the model to properly categorize and match new messages with appropriate tags and keywords as the user's 
journey evolves. The key idea here is that memory importance is not the same as semantic similarity.

A third layer of LLM reasoning will also be used to plan the context injection based on an evolving governance policy.
When deciding what context to surface, the governance policy will balance factors such as: 
- affirmation versus challenge
- continuity versus novelty, 
- immediate relevance versus long-term growth, 
- individual experience versus broader external perspective. 

This agentic layer will also reason over sequencing decisions and schedule revisits to key insights
and breakthroughs from the user's journey to date.

In summary, LLM use will be layered in three key ways:

1. Reasoning — answers the present question with past context bundled.
2. Memory structuring — classifies and preserves the past.
3. Planning / Sequencing — decides how the past should influence the future.

```text
                         User
                           │
                           ▼
              Mobile Web Interface
                     (HTML/JS)
                           │
                           ▼
                      FastAPI API
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
     Memory Structuring LLM    Planning / Sequencing LLM
        (Classification)          (Context Governance)
          ▲        │                       │
          │        ▼                       ▼
   User Profile  MongoDB             Retrieval Layer (RAG)
                 (Memory)                  │
                     │                     │
                     └──────────┬──────────┘
                                │
                                ▼
                       Curated Past Context
                                │
                                ▼
                          Reasoning LLM
                             (OpenAI)
                                │
                                ▼
                          User Response
```


