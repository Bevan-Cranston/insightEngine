import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langchain_core.chat_history import InMemoryChatMessageHistory


from app.db import InsightEngineDB
from app.retrieval import SemanticRetriever


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class InsightEngineServer:
    def __init__(self):
        load_dotenv()

        self.app = FastAPI(title="Insight Engine")
        self.model_name = "gpt-5-mini"
        self.embedding_model_name = "all-MiniLM-L6-v2"
        self.llm = ChatOpenAI(model=self.model_name, temperature=0.7, api_key=os.getenv("OPENAI_API_KEY"))
        self.retriever = SemanticRetriever(self.embedding_model_name)
        self.db = InsightEngineDB()

        self.base_dir = Path(__file__).resolve().parent
        self.system_prompt_version = "v2"

        self.system_prompt = (
            "You are Insight Engine, a reflective thought partner. "
            "Help the user explore their thoughts clearly to generate useful insight. "
            "Be concise, grounded, and ask thoughtful questions when useful." 
            "Default to concise responses that encourage reflection and conversation rather than lengthy explanations."
        )

        self._register_routes()

        self.histories = {}
        self.memory_window_size = 5
        self.all_stored_messages = self.db.get_all_messages()

    def _register_routes(self):
        @self.app.get("/")
        def serve_homepage():
            html_path = self.base_dir / "static" / "index.html"
            return FileResponse(html_path)

        @self.app.post("/chat")
        def chat(request: ChatRequest):
            conversation_id = request.conversation_id

            user_message = request.message

            user_embedding = self.retriever.create_embedding(user_message)

            k_most_relevant = self.retriever.search(user_embedding, self.all_stored_messages)

            messages = [
                SystemMessage(content=self.system_prompt),
                *k_most_relevant
            ]

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

            messages.extend(history.messages[-self.memory_window_size:])
            messages.append(user_message)

            history.add_user_message(user_message)

            response = self.llm.invoke(messages)
            reply = response.content

            assistant_embedding = self.retriever.create_embedding(reply)

            history.add_ai_message(reply)

            self.db.save_chat_turn(
                conversation_id=request.conversation_id,
                user_message=request.message,
                user_embedding=user_embedding,
                assistant_message=reply,
                assistant_embedding=assistant_embedding,
                model_name=self.model_name,
                embedding_model_name=self.embedding_model_name,
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
            self.all_stored_messages = self.db.get_all_messages()
            next_conversation = self.db.create_next_conversation()
            return {
                "conversation_id": next_conversation['conversation_id'],
                "conversation_title": next_conversation['conversation_title']
            }

        @self.app.delete("/conversations")
        def delete_all_conversations():
            self.db.reset_db()
            self.histories.clear()

            return {
                "success": True,
                "message": "All conversations and messages deleted."
            }

        @self.app.get("/conversations/{conversation_id}/messages")
        def get_conversation_messages(conversation_id: str):
            return self.db.get_messages_for_conversation(conversation_id)


server = InsightEngineServer()
app = server.app
