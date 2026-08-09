export interface ChatRequest {
  conversation_id: string | undefined;
  question: string;
}

export interface SourceItem {
  document_name: string;
  chunk_index: number;
}

export interface ChatResponse {
  conversation_id: string;
  answer: string;
  sources: SourceItem[];
}

export type ChatRole = "USER" | "ASSISTANT";

export interface ChatRequest {
  conversation_id: string | undefined;
  question: string;
}

export interface ChatMessage {
  role: ChatRole;
  content: string;
  sources?: SourceItem[];
}
