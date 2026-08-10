# ADR-002: Use MongoDB for persistent message storage

## Status
Accepted

## Context
Memory is a key feature of insight engine, requiring persistent storage of conversation messages. By default, API based
chat systems are stateless and so some sort of storage system is required.

Early development could have used file-based storage such as JSON, however the planned memory architecture requires 
messages and associated metadata to be queried, updated, and retrieved across conversations,
therefore a database was selected as the persistent storage layer.

## Decision

Adopt MongoDB as the primary persistent database for conversation messages and associated memory metadata.

Messages and associated metadata will be stored together as individual documents rather than spread across an SQL-style 
relational schema.

## Reasons

MongoDB's flexible document model will be useful during development of the custom memory architecture, e.g.
the current message schema is:
```json
{
  "conversation_id": "...",
  "role": "user",
  "content": "...",
  "created_at": "...",
  "model": null,
  "system_prompt_version": null,
  "tags": [],
  "embedding": null,
  "embedding_model": null
}
```
But a future version could easily be:
```
message
├── conversation_id
├── role
├── content
├── timestamp
├── model
├── system prompt version
├── embedding
├── embedding model
├── keywords[]
├── themes[]
├── importance
├── recurring_patterns[]
├── unresolved_friction
├── revisit_timing
└── ...
```
This is a particularly attractive feature, as memory structuring is an active area of product development and will likely
continue to be so, with memory architecture being a core pillar of product value.

The main relational consideration in the current system is which conversation a message belongs to, therefore more 
sophisticated SQL-style relational arrangements were deemed unnecessary at this stage. 

## Trade-offs

- Reduced schema enforcement compared with a relational database.
- Flexible schemas can lead to inconsistent document structures if not controlled at the application layer.
- Some future features may be better suited to relational modelling, for example:
```
Insight Engine
     │
     ├── MongoDB
     │    └── conversational memory
     │
     └── PostgreSQL
          └── users / billing / permissions / etc.
```
## Consequences

MongoDB will be used for all current persistent data storage. 
In the future, a system such as PostgreSQL may be considered as user separation becomes explicit and additional 
relational functionality requires support. MongoDB will remain the primary storage system for conversational memory 
unless future requirements justify revisiting this decision.