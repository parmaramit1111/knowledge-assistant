import { Person, SmartToy } from "@mui/icons-material";
import { Avatar, Box, Paper, Stack, Typography } from "@mui/material";

interface ChatMessageProps {
  role: "USER" | "ASSISTANT";
  content: string;
  isLoading?: boolean;
}

export default function ChatMessage({ role, content, isLoading = false }: ChatMessageProps) {
  const isUser = role === "USER";

  return (
    <Stack
      direction="row"
      spacing={2}
      sx={{
        width: "100%",
        maxWidth: 900,
        mx: "auto",
        px: { xs: 2, md: 3 },
        py: 2,
        alignItems: "flex-start",
      }}
    >
      <Avatar
        sx={{
          width: 34,
          height: 34,
          bgcolor: isUser ? "secondary.main" : "primary.main",
        }}
      >
        {isUser ? <Person fontSize="small" /> : <SmartToy fontSize="small" />}
      </Avatar>

      <Box sx={{ flex: 1, minWidth: 0 }}>
        <Typography variant="subtitle2" sx={{ mb: 0.5, fontWeight: 700 }}>
          {isUser ? "You" : "Knowledge Assistant"}
        </Typography>

        <Paper
          elevation={0}
          sx={{
            p: isUser ? 1.5 : 0,
            bgcolor: isUser ? "action.hover" : "transparent",
            borderRadius: isUser ? 2 : 0,
          }}
        >
          {isLoading ? (
            <Stack direction="row" spacing={0.5}>
              <Typography color="text.secondary">●</Typography>
              <Typography color="text.secondary">●</Typography>
              <Typography color="text.secondary">●</Typography>
            </Stack>
          ) : (
            <Typography
              variant="body1"
              color="text.primary"
              sx={{
                whiteSpace: "pre-wrap",
                wordBreak: "break-word",
              }}
            >
              {content}
            </Typography>
          )}
        </Paper>
      </Box>
    </Stack>
  );
}
