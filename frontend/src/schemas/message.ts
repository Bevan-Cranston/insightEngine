import { z } from "zod";

export const MessageSchema = z.object({
  role: z.string(),
  content: z.string(),
  created_at: z.string(),
});

export const MessagesSchema = z.array(MessageSchema);

export type Message = z.infer<typeof MessageSchema>;