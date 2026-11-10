import { useEffect, useState } from "react";
import { getConversations } from "../api/client";
import type { Conversation } from "../schemas/conversation";

type ConversationListProps = {
  onSelectConversation: (id: string) => void;
};

function ConversationList({
  onSelectConversation,
}: ConversationListProps) {
  const [conversations, setConversations] =
    useState<Conversation[]>([]);

  useEffect(() => {
    async function loadConversations() {
      const data = await getConversations();
      setConversations(data);
    }

    loadConversations().catch(console.error);
  }, []);

  return (
    <section>
      <h2>Conversations</h2>

      {conversations.map((conversation) => (
        <button
          key={conversation.id}
          onClick={() => onSelectConversation(conversation.id)}
        >
          {conversation.title}
        </button>
      ))}
    </section>
  );
}

export default ConversationList;