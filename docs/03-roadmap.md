# Insight Engine Roadmap

This document outlines the planned development of Insight Engine beyond the initial MVP. The roadmap is intended to 
outline current priorities and a forward looking pathway rather than serve as a fixed commitment to specific features 
or timelines.

Work is organized by engineering area rather than a strict release order, allowing priorities to evolve as the project develops.

## Current State - MVP+

Insight Engine currently provides:

- FastAPI backend
- OpenAI LLM integration via LangChain
- LangChain-based message orchestration 
- MongoDB persistent conversation storage
- Mobile browser-based interface (HTML, CSS and JS)
- In-chat conversational memory
- Semantic-based retrieval of similar messages from previous conversations
- Containerized application layer with Docker 

## Selected Next Stage Tasks

- Containerize Mongo
- Resolve Github issues relating to conversation initialization and storage
- Typescript frontend
- Improve chat interface and conversation navigation

Note: These tasks are referenced from the following categories with a check beside denoting it is currently scheduled.
Once the selected task is complete, move it up to Current State.

## AI Systems Engineering

This area focuses on improving long-term memory, retrieval quality and interaction with large language models.

- [ ] Develop keyword extraction architecture
- [ ] Hybrid retrieval (semantic + keyword/tag-based)
- [ ] Develop context governance for retrieval prompt injection
- [ ] Develop Agentic framework around sequencing and retrieval

## Backend Engineering

This area focuses on reliability engineering and supporting the addition of new product features 

- [x] Resolve Github issues relating to conversation initialization and storage
- [ ] Develop user separation functionality with login and authentication

## Frontend Engineering

This area focuses on improving the user experience and providing a clean and intuitive interface for application features.

- [x] Typescript frontend
- [x] Improve chat interface and conversation navigation

## Data Engineering

This area focuses on structuring data to support new features.

- [ ] Design metadata schema for keyword search
- [ ] Design metadata schema for user profiles
- [ ] Ranking strategy for retrieved memories

## Deployment & Operations

This area covers how Insight Engine is packaged, deployed, monitored and maintained across development and production environments.

- [x] Containerize Mongo 
- [ ] Centralized application logging and monitoring
- [ ] Upload to AWS via ECR and test on EC2 with S3 volume

## Guiding Principles

The roadmap is organised around engineering disciplines rather
than fixed release versions.

This reflects the belief that software systems mature across multiple areas
simultaneously. As Insight Engine evolves, work will likely progress in parallel across these areas rather than sequentially.

Consequently, this roadmap should be viewed as a living engineering document
rather than a fixed development schedule.