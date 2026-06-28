from datetime import datetime, timezone
from copy import deepcopy
import json
from pathlib import Path

from pymongo import MongoClient


def utc_now():
    return datetime.now(timezone.utc).isoformat()


class SchemaLoader:
    def __init__(self):
        self.schema_dir = Path(__file__).resolve().parent.parent / "schemas"
        self.conversation_template = self._load_json("conversation.json")
        self.message_template = self._load_json("message.json")

    def _load_json(self, filename):
        with open(self.schema_dir / filename, "r", encoding="utf-8") as f:
            return json.load(f)

    def new_conversation(self):
        return deepcopy(self.conversation_template)

    def new_message(self):
        return deepcopy(self.message_template)


class InsightEngineDB:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017")
        self.db = self.client["insight_engine"]
        self.conversations = self.db["conversations"]
        self.messages = self.db["messages"]
        self.schemas = SchemaLoader()

    def reset_db(self):
        archive_db = self.client["insight_engine_dev"]
        archive_db.messages.insert_many(list(self.messages.find({})))
        archive_db.conversations.insert_many(list(self.conversations.find({})))
        self.conversations.delete_many({})
        self.messages.delete_many({})

    def create_conversation(self, title="New Chat"):
        now = utc_now()

        conversation = self.schemas.new_conversation()
        conversation["title"] = title
        conversation["created_at"] = now
        conversation["updated_at"] = now

        result = self.conversations.insert_one(conversation)
        return {"conversation_id": str(result.inserted_id), "conversation_title": title}

    def create_next_conversation(self):
        count = self.conversations.count_documents({})
        title = f"New Chat {count + 1}"
        return self.create_conversation(title=title)

    def get_conversations(self):
        return [
            {
                "id": str(conversation["_id"]),
                "title": conversation["title"]
            }
            for conversation in self.conversations.find({})
        ]

    def create_message(
        self,
        conversation_id,
        role,
        content,
        embedding,
        model_name=None,
        embedding_model_name=None,
        system_prompt_version=None,
    ):
        message = self.schemas.new_message()
        message["conversation_id"] = conversation_id
        message["role"] = role
        message["content"] = content
        message["embedding"] = embedding
        message["created_at"] = utc_now()
        message["model"] = model_name
        message["embedding_model_name"] = embedding_model_name
        message["system_prompt_version"] = system_prompt_version

        self.messages.insert_one(message)

    def save_chat_turn(
        self,
        conversation_id,
        user_message,
        user_embedding,
        assistant_message,
        assistant_embedding,
        model_name,
        embedding_model_name,
        system_prompt_version,
    ):
        if conversation_id is None:
            conversation_id = self.create_next_conversation()["conversation_id"]

        self.create_message(
            conversation_id=conversation_id,
            role="user",
            content=user_message,
            embedding=user_embedding,
            embedding_model_name=embedding_model_name
        )

        self.create_message(
            conversation_id=conversation_id,
            role="assistant",
            content=assistant_message,
            embedding=assistant_embedding,
            model_name=model_name,
            embedding_model_name=embedding_model_name,
            system_prompt_version=system_prompt_version,
        )

        self.conversations.update_one(
            {"_id": self._to_object_id(conversation_id)},
            {"$set": {"updated_at": utc_now()}},
        )

        return conversation_id

    def get_messages_for_conversation(self, conversation_id):
        return [
            {
                "role": msg["role"],
                "content": msg["content"],
                "created_at": msg["created_at"]
            }
            for msg in self.messages.find(
                {"conversation_id": conversation_id}
            ).sort("created_at", 1)
        ]

    def get_recent_messages(self, conversation_id, limit=20):
        messages = self.get_messages_for_conversation(conversation_id)
        return messages[-limit:]

    def get_all_messages(self):
        return [
            msg for msg in self.messages.find({})]

    def _to_object_id(self, id_string):
        from bson import ObjectId
        return ObjectId(id_string)

