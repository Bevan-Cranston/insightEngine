import { useState } from "react";
import ConversationList from "./components/ConversationList";
import ConversationWindow from "./components/ConversationWindow";

function App() {
  const [currentConversationId, setCurrentConversationId] =
    useState<string | null>(null);

  return (
    <main>
      <h1>Insight Engine</h1>

      <ConversationList
        onSelectConversation={setCurrentConversationId}
      />

      <ConversationWindow
        key={currentConversationId ?? "none"}
        conversationId={currentConversationId}
      />
    </main>
  );
}

export default App;