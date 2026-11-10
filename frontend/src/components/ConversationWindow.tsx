import { useEffect, useState } from "react";
import { getMessages } from "../api/client";
import type { Message } from "../schemas/message";


type ConversationWindowProps = {
  conversationId: string | null;
};

function ConversationWindow({
  conversationId,
}: ConversationWindowProps) {
  const [messages, setMessages] = useState<Message[]>([]);

  useEffect(() => {
    if (!conversationId) {
      return;
    }

    async function loadMessages() {
        const data = await getMessages(conversationId!);
        setMessages(data);
    }

    loadMessages().catch(console.error);
}, [conversationId]);

  if (!conversationId) {
    return <p>No conversation selected.</p>;
  }

  return (
    <section>
      <h2>Conversation</h2>

      {messages.map((message, index) => (
        <p key={index}>
          <strong>{message.role}:</strong> {message.content}
        </p>
      ))}
    </section>
  );
}

export default ConversationWindow;