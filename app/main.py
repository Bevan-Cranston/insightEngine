import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.chat_history import InMemoryChatMessageHistory


from app.db import InsightEngineDB


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class InsightEngineServer:
    def __init__(self):
        load_dotenv()

        self.app = FastAPI(title="Insight Engine")
        self.model = "gpt-5-mini"
        self.llm = ChatOpenAI(model=self.model, temperature=0.7, api_key=os.getenv("OPENAI_API_KEY"))
        self.db = InsightEngineDB()

        self.base_dir = Path(__file__).resolve().parent
        self.system_prompt_version = "v1"

        self.system_prompt = (
            "You are Insight Engine, a reflective thought partner. "
            "Help the user explore their thoughts clearly and generate useful insight. "
            "Be concise, grounded, and ask thoughtful questions when useful."
        )

        self._register_routes()

        self.histories = {}
        self.memory_window_size = 5

    def _register_routes(self):
        @self.app.get("/")
        def serve_homepage():
            html_path = self.base_dir / "static" / "index.html"
            return FileResponse(html_path)

        @self.app.post("/chat")
        def chat(request: ChatRequest):
            conversation_id = request.conversation_id

            if conversation_id is None:
                conversation = self.db.create_next_conversation()
                conversation_id = conversation["conversation_id"]

            if conversation_id not in self.histories:
                history = InMemoryChatMessageHistory()

                recent_messages = self.db.get_recent_messages(
                    conversation_id=conversation_id,
                    limit=self.memory_window_size,
                )

                for message in recent_messages:
                    if message["role"] == "user":
                        history.add_user_message(message["content"])
                    elif message["role"] == "assistant":
                        history.add_ai_message(message["content"])

                self.histories[conversation_id] = history

            history = self.histories[conversation_id]

            messages = [
                SystemMessage(content=self.system_prompt),
                *history.messages[-self.memory_window_size:],
            ]

            history.add_user_message(request.message)
            messages.append(history.messages[-1])

            response = self.llm.invoke(messages)
            reply = response.content

            history.add_ai_message(reply)

            reply = response.content

            self.db.save_chat_turn(
                conversation_id=request.conversation_id,
                user_message=request.message,
                assistant_message=reply,
                model=self.model,
                system_prompt_version=self.system_prompt_version,
            )

            return {
                "reply": reply,
                "conversation_id": conversation_id,
            }

        @self.app.get("/conversations")
        def get_conversations():
            return self.db.get_conversations()

        @self.app.post("/conversations")
        def create_conversation():
            next_conversation = self.db.create_next_conversation()
            return {
                "conversation_id": next_conversation['conversation_id'],
                "conversation_title": next_conversation['conversation_title']
            }

        @self.app.get("/conversations/{conversation_id}/messages")
        def get_conversation_messages(conversation_id: str):
            return self.db.get_messages_for_conversation(conversation_id)


server = InsightEngineServer()
app = server.app
