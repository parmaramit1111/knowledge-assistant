const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "/api/v1";
import { ApiResponse } from "./models/apiResponse";
import { ChatRequest, ChatResponse } from "./models/chat";

export async function askQuestion(request: ChatRequest): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/chat/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`Chat request failed with status ${response.status}`);
  }

  const result: ApiResponse<ChatResponse> = await response.json();

  if (!result.success) {
    throw new Error(result.message);
  }

  return result.result;
}
