import { useCallback, useState } from "react";

import { askQuestion } from "../api/chat";
import { ChatMessage, ChatResponse } from "../api/models/chat";

export interface UseChatResult {
  messages: ChatMessage[];
  conversationId: string | null;
  isLoading: boolean;
  error: string | null;
  askQuestion: (question: string) => Promise<void>;
  newConversation: () => void;
}

export function useChat(): UseChatResult {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(null);

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAskQuestion = useCallback(
    async (question: string): Promise<void> => {
      const trimmedQuestion = question.trim();

      if (!trimmedQuestion || isLoading) {
        return;
      }

      setError(null);

      const userMessage: ChatMessage = {
        role: "USER",
        content: trimmedQuestion,
        sources: [],
      };

      setMessages((current) => [...current, userMessage]);

      setIsLoading(true);

      try {
        const response: ChatResponse = await askQuestion({
          question: trimmedQuestion,
          conversation_id: conversationId ?? undefined,
        });

        setConversationId(response.conversation_id);

        const assistantMessage: ChatMessage = {
          role: "ASSISTANT",
          content: response.answer,
          sources: response.sources,
        };

        setMessages((current) => [...current, assistantMessage]);
      } catch (err) {
        const message = err instanceof Error ? err.message : "Unable to process your question.";

        setError(message);
      } finally {
        setIsLoading(false);
      }
    },
    [conversationId, isLoading],
  );

  const newConversation = useCallback(() => {
    setMessages([]);
    setConversationId(null);
    setError(null);
    setIsLoading(false);
  }, []);

  return {
    messages,
    conversationId,
    isLoading,
    error,
    askQuestion: handleAskQuestion,
    newConversation,
  };
}
