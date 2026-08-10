import { DescriptionOutlined } from "@mui/icons-material";
import { Box, Chip, Stack, Typography } from "@mui/material";

interface ChatSource {
  document_name: string;
  chunk_index: number;
}

interface ChatSourcesProps {
  sources: ChatSource[];
}

export default function ChatSources({ sources }: ChatSourcesProps) {
  if (!sources.length) {
    return null;
  }

  return (
    <Box sx={{ mt: 2 }}>
      <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 700 }}>
        Sources
      </Typography>

      <Stack useFlexGap sx={{ direction: "row", spacing: 1, flexWrap: "wrap" }}>
        {sources.map((source, index) => (
          <Chip
            key={`${source.document_name}-${source.chunk_index}-${index}`}
            icon={<DescriptionOutlined />}
            label={`${source.document_name} · Chunk ${source.chunk_index}`}
            variant="outlined"
            size="small"
            sx={{
              maxWidth: "100%",
              "& .MuiChip-label": {
                overflow: "hidden",
                textOverflow: "ellipsis",
              },
            }}
          />
        ))}
      </Stack>
    </Box>
  );
}
