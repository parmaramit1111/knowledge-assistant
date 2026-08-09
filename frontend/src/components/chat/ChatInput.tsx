import { ArrowUpward } from "@mui/icons-material";
import { IconButton, Paper, TextField } from "@mui/material";
import { KeyboardEvent, useState } from "react";

interface ChatInputProps {
  onSend: (question: string) => Promise<void>;
  disabled?: boolean;
}

export default function ChatInput({ onSend, disabled = false }: ChatInputProps) {
  const [question, setQuestion] = useState("");

  const handleSend = async () => {
    const value = question.trim();

    if (!value || disabled) {
      return;
    }

    setQuestion("");

    try {
      await onSend(value);
    } catch {
      setQuestion(value);
    }
  };

  const handleKeyDown = (event: KeyboardEvent<HTMLDivElement>) => {
    if (event.key !== "Enter") {
      return;
    }

    if (event.shiftKey) {
      return;
    }

    event.preventDefault();

    void handleSend();
  };

  return (
    <Paper
      component="form"
      onSubmit={(event) => {
        event.preventDefault();
        void handleSend();
      }}
      elevation={0}
      sx={{
        display: "flex",
        alignItems: "flex-end",
        gap: 1,
        width: "100%",
        maxWidth: 900,
        mx: "auto",
        p: 1,
        border: 1,
        borderColor: "divider",
        borderRadius: 3,
        bgcolor: "background.paper",
        boxShadow: "0 2px 8px rgba(0, 0, 0, 0.06)",
      }}
    >
      <TextField
        fullWidth
        multiline
        maxRows={6}
        value={question}
        disabled={disabled}
        placeholder="Ask anything about your documents..."
        onChange={(event) => setQuestion(event.target.value)}
        onKeyDown={handleKeyDown}
        variant="standard"
        slotProps={{
          input: {
            disableUnderline: true,
          },
        }}
        sx={{
          px: 1,
        }}
      />

      <IconButton
        type="submit"
        disabled={!question.trim() || disabled}
        color="primary"
        sx={{
          width: 40,
          height: 40,
          bgcolor: "primary.main",
          color: "primary.contrastText",

          "&:hover": {
            bgcolor: "primary.dark",
          },

          "&.Mui-disabled": {
            bgcolor: "action.disabledBackground",
            color: "action.disabled",
          },
        }}
      >
        <ArrowUpward fontSize="small" />
      </IconButton>
    </Paper>
  );
}
