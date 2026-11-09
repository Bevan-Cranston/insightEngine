import { z } from "zod";

export const ConversationSchema = z.object({
  id: z.string(),
  title: z.string(),
});

export const ConversationsSchema =
  z.array(ConversationSchema);

export type Conversation =
  z.infer<typeof ConversationSchema>;