import type { ApiResponse } from "./models/apiResponse";
import type { DocumentUploadResponse } from "./models/document";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "/api/v1";

export async function uploadDocument(file: File): Promise<DocumentUploadResponse> {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/documents/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Document upload failed with status ${response.status}`);
  }

  const result: ApiResponse<DocumentUploadResponse> = await response.json();

  if (!result.success) {
    throw new Error(result.message);
  }

  return result.result;
}
