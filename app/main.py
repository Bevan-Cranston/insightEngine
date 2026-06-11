import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai import OpenAI


class ChatRequest(BaseModel):
    message: str


class InsightEngineServer:
    def __init__(self):
        load_dotenv()

        self.app = FastAPI(title="Insight Engine")
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.base_dir = Path(__file__).resolve().parent
        self.system_prompt = (
            "You are Insight Engine, a reflective thought partner. "
            "Help the user explore their thoughts clearly and generate useful insight. "
            "Be concise, grounded, and ask thoughtful questions when useful."
        )

        self._register_routes()

    def _register_routes(self):
        @self.app.get("/")
        def serve_homepage():
            html_path = self.base_dir / "static" / "index.html"
            return FileResponse(html_path)

        @self.app.post("/chat")
        def chat(request: ChatRequest):
            response = self.client.responses.create(
                model="gpt-5-mini",
                input=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": request.message},
                ],
            )

            return {"reply": response.output_text}


server = InsightEngineServer()
app = server.app