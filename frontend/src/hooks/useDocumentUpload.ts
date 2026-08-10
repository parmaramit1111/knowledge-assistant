import { useState } from "react";

import { uploadDocument } from "../api/document";

export function useDocumentUpload() {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const clearUploadStatus = (): void => {
    setError(null);
    setSuccessMessage(null);
  };

  const upload = async (file: File): Promise<void> => {
    setUploading(true);
    setError(null);
    setSuccessMessage(null);

    try {
      const response = await uploadDocument(file);

      setSuccessMessage(response.message ?? "Document uploaded successfully.");
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to upload document.";

      setError(message);
    } finally {
      setUploading(false);
    }
  };

  return {
    uploading,
    error,
    successMessage,
    upload,
    clearUploadStatus,
  };
}
