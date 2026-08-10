import { useState } from "react";
import { Box } from "@mui/material";

import ChatContainer from "../components/chat/ChatContainer";
import ChatHeader from "../components/chat/ChatHeader";
import ChatSidebar from "../components/chat/ChatSidebar";
import DocumentUpload from "../components/documents/DocumentUpload";

import { useChat } from "../hooks/useChat";
import { useDocumentUpload } from "../hooks/useDocumentUpload";

type ActiveView = "chat" | "upload";

export default function ChatPage() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [activeView, setActiveView] = useState<ActiveView>("chat");

  const { messages, conversationId, isLoading, error, askQuestion, newConversation } = useChat();

  const { uploading, error: uploadError, successMessage, upload, clearUploadStatus } = useDocumentUpload();

  const handleNewChat = (): void => {
    newConversation();
    setActiveView("chat");
    clearUploadStatus();
  };

  const handleUploadComplete = (): void => {
    setActiveView("upload");
  };

  return (
    <Box
      sx={{
        height: "100vh",
        display: "flex",
        overflow: "hidden",
        bgcolor: "background.default",
      }}
    >
      {/* ============================================================ */}
      {/* Sidebar */}
      {/* ============================================================ */}

      <ChatSidebar
        open={true}
        collapsed={sidebarCollapsed}
        conversationId={conversationId}
        onNewChat={handleNewChat}
        onClose={() => setSidebarCollapsed(true)}
        onToggle={() => setSidebarCollapsed((current) => !current)}
        onUploadDocuments={() => {
          clearUploadStatus();
          setActiveView("upload");
        }}
      />

      {/* ============================================================ */}
      {/* Main Content */}
      {/* ============================================================ */}

      <Box
        sx={{
          flex: 1,
          minWidth: 0,
          display: "flex",
          flexDirection: "column",
          height: "100vh",
        }}
      >
        <ChatHeader sidebarOpen={!sidebarCollapsed} onMenuClick={() => setSidebarCollapsed(false)} />

        <Box
          sx={{
            flex: 1,
            minHeight: 0,
            overflow: "auto",
          }}
        >
          {activeView === "upload" ? <DocumentUpload uploading={uploading} error={uploadError} successMessage={successMessage} onUpload={upload} /> : <ChatContainer messages={messages} isLoading={isLoading} error={error} onSend={askQuestion} />}
        </Box>
      </Box>
    </Box>
  );
}
