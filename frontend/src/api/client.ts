import { MessagesSchema } from "../schemas/message";

export async function getMessages(conversationId: string) {
  const response = await fetch(
    `/conversations/${encodeURIComponent(conversationId)}/messages`
  );

  if (!response.ok) {
    throw new Error("Failed to retrieve messages");
  }

  const data: unknown = await response.json();

  return MessagesSchema.parse(data);
}

import { ConversationsSchema } from "../schemas/conversation";

export async function getConversations() {
  const response = await fetch("/conversations");

  if (!response.ok) {
    throw new Error("Failed to load conversations");
  }

  const data: unknown = await response.json();

  return ConversationsSchema.parse(data);
}
