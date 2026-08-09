import { Alert, Box, CircularProgress, Stack } from "@mui/material";

import ChatInput from "./ChatInput";
import ChatMessage from "./ChatMessage";
import ChatSources from "./ChatSources";

interface ChatMessageModel {
  role: "USER" | "ASSISTANT";
  content: string;
  sources?: {
    document_name: string;
    chunk_index: number;
  }[];
}

interface ChatContainerProps {
  messages: ChatMessageModel[];
  isLoading: boolean;
  error: string | null;
  onSend: (question: string) => Promise<void>;
}

export default function ChatContainer({ messages, isLoading, error, onSend }: ChatContainerProps) {
  return (
    <Box
      sx={{
        flex: 1,
        minHeight: 0,
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* Messages */}
      <Box
        sx={{
          flex: 1,
          overflowY: "auto",
          py: 2,
        }}
      >
        {messages.length === 0 ? (
          <Stack
            sx={{
              alignItems: "center",
              justifyContent: "center",
              height: "100%",
              px: 2,
              textAlign: "center",
            }}
          >
            <Box
              sx={{
                maxWidth: 600,
              }}
            >
              <Box
                component="div"
                sx={{
                  width: 56,
                  height: 56,
                  mx: "auto",
                  mb: 2,
                  borderRadius: "50%",
                  bgcolor: "primary.main",
                  color: "primary.contrastText",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: 26,
                  fontWeight: 700,
                }}
              >
                K
              </Box>

              <Box
                component="h1"
                sx={{
                  m: 0,
                  mb: 1,
                  fontSize: {
                    xs: "1.5rem",
                    md: "2rem",
                  },
                  fontWeight: 700,
                  color: "text.primary",
                }}
              >
                How can I help you?
              </Box>

              <Box
                component="p"
                sx={{
                  m: 0,
                  color: "text.secondary",
                  fontSize: "0.95rem",
                }}
              >
                Ask questions about your documents and get grounded answers with source references.
              </Box>
            </Box>
          </Stack>
        ) : (
          <>
            {messages.map((message, index) => (
              <ChatMessage key={`${message.role}-${index}`} role={message.role} content={message.content} />
            ))}

            {isLoading && <ChatMessage role="ASSISTANT" content="" isLoading />}

            {error && (
              <Box
                sx={{
                  width: "100%",
                  maxWidth: 900,
                  mx: "auto",
                  px: { xs: 2, md: 3 },
                  py: 1,
                }}
              >
                <Alert severity="error">{error}</Alert>
              </Box>
            )}
          </>
        )}
      </Box>

      {/* Composer */}
      <Box
        sx={{
          px: { xs: 1.5, md: 2 },
          pt: 1,
          pb: 2,
          bgcolor: "background.default",
        }}
      >
        <ChatInput onSend={onSend} disabled={isLoading} />

        <Box
          sx={{
            mt: 1,
            textAlign: "center",
            fontSize: "0.7rem",
            color: "text.secondary",
          }}
        >
          Knowledge Assistant can make mistakes. Verify important information.
        </Box>
      </Box>
    </Box>
  );
}
