# Insight Engine

A conversational system for personalized insight extraction and development built on a FastAPI server using OpenAI API with MongoDB backend storage.

Note: to start server, run the following command in root:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

## Project Roadmap

### V1 - MVP

- [x] FastAPI server
- [x] OpenAI integration
- [x] HTML interface
- [x] MongoDB schema design
- [x] MongoDB storage
- [x] In chat memory

### V2 - Retrieval

- [ ] Tag extraction
- [ ] Retrieval based on tags 
- [ ] Retrieval on semantic similarity

### Testing and Research

- [ ] System message development
- [ ] Tag structure development
- [ ] Retrieval injection methodology

```text
Phone Browser
      ↓
   FastAPI
   ↙     ↘
OpenAI   MongoDB
```