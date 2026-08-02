# ADR-001: Use LangChain for LLM orchestration

## Status
Accepted

## Context
The first version of Insight Engine called the OpenAI API directly, however once LangChain was investigated it was 
understood that it could provide an interface with the OpenAI LLM, as well as enabling future capabilities. 

## Decision
Adopt LangChain as the project's primary LLM orchestration framework.

This replaces direct interaction with the OpenAI Python client while
maintaining compatibility with OpenAI models.

Replace:
```python
from openai import OpenAI
```

With:
```python
from langchain_openai import ChatOpenAI
```

## Reasons
- Conversational memory was always going to be a core product feature and something that would be explored in depth
- LangChain provides a tidy abstraction for chaining message history together: LLMChain
- Although it would've been possible to store live conversation history in a simple Python list, LangChain provides features that could be useful for future agentic workflows
- Also offers support to switch models and providers interchangeably for experiments

## Trade-offs
- Additional abstraction
- More overhead with the larger package size
- Possible difficulty understanding underlying behaviour
- Framework changes may introduce maintenance work

## Consequences

- Future LLM functionality should be implemented through LangChain rather than direct OpenAI API calls.
- Future retrieval and memory features can build on LangChain abstractions.
- Changes to LangChain may occasionally require project updates when new versions are released.
