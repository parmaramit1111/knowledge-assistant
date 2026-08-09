import { Add, ChatBubbleOutlined, CloudUploadOutlined, MenuOpen, MenuOutlined, AccessTime } from "@mui/icons-material";
import { Box, Button, Divider, IconButton, Stack, Typography } from "@mui/material";

import { BrandLogo } from "../common/BrandLogo";

interface ChatSidebarProps {
  open: boolean;
  collapsed: boolean;
  conversationId: string | null;
  onNewChat: () => void;
  onClose: () => void;
  onToggle: () => void;
  onUploadDocuments: () => void;
}

export default function ChatSidebar({ open, collapsed, conversationId, onNewChat, onClose, onToggle, onUploadDocuments }: ChatSidebarProps) {
  if (!open) {
    return null;
  }

  const sidebarWidth = collapsed ? 76 : 318;

  return (
    <Box
      component="aside"
      sx={{
        width: sidebarWidth,
        height: "100vh",
        flexShrink: 0,
        display: "flex",
        flexDirection: "column",
        bgcolor: "background.paper",
        borderRight: 1,
        borderColor: "divider",
        overflow: "hidden",
        transition: "width 0.2s ease",
      }}
    >
      {/* ---------------------------------------------------------------- */}
      {/* Brand Header */}
      {/* ---------------------------------------------------------------- */}

      <Box
        sx={{
          minHeight: 118,
          px: collapsed ? 1.5 : 3,
          py: 2.5,
          display: "flex",
          alignItems: "center",
          justifyContent: collapsed ? "center" : "space-between",
        }}
      >
        {!collapsed ? <BrandLogo collapsed={false} height={72} /> : <BrandLogo collapsed height={42} />}

        {!collapsed && (
          <IconButton
            size="small"
            onClick={onClose}
            aria-label="Collapse sidebar"
            sx={{
              color: "text.secondary",
            }}
          >
            <MenuOpen />
          </IconButton>
        )}

        {collapsed && (
          <IconButton
            size="small"
            onClick={onToggle}
            aria-label="Expand sidebar"
            sx={{
              position: "absolute",
              left: 58,
              top: 32,
              bgcolor: "background.paper",
              border: 1,
              borderColor: "divider",
              zIndex: 2,
            }}
          >
            <MenuOutlined fontSize="small" />
          </IconButton>
        )}
      </Box>

      <Divider />

      {/* ---------------------------------------------------------------- */}
      {/* Actions */}
      {/* ---------------------------------------------------------------- */}

      <Stack
        spacing={1.25}
        sx={{
          px: collapsed ? 0.7 : 3,
          py: 2.5,
        }}
      >
        {/* New Chat */}
        <Button
          fullWidth
          variant="contained"
          startIcon={<Add />}
          onClick={onNewChat}
          sx={{
            minHeight: 45,
            justifyContent: collapsed ? "center" : "flex-start",
            px: collapsed ? 1 : 2,
            borderRadius: 1,
            fontSize: 16,
            fontWeight: 600,
            textTransform: "none",
            boxShadow: "none",
            background: "linear-gradient(135deg, #2979ff 0%, #1565f0 100%)",
            "&:hover": {
              boxShadow: "none",
              background: "linear-gradient(135deg, #1565f0 0%, #0d47c7 100%)",
            },
            "& .MuiButton-startIcon": {
              mr: collapsed ? 0 : 1,
            },
          }}
        >
          {!collapsed && "New Chat"}
        </Button>

        {/* Upload Documents */}
        <Button
          fullWidth
          variant="outlined"
          startIcon={<CloudUploadOutlined />}
          onClick={onUploadDocuments}
          sx={{
            minHeight: 45,
            justifyContent: collapsed ? "center" : "flex-start",
            px: collapsed ? 1 : 2,
            borderRadius: 1,
            fontSize: 16,
            fontWeight: 600,
            textTransform: "none",
            borderWidth: 1.5,
            "& .MuiButton-startIcon": {
              mr: collapsed ? 0 : 1,
            },
          }}
        >
          {!collapsed && "Upload Documents"}
        </Button>
      </Stack>

      <Divider />

      {/* ---------------------------------------------------------------- */}
      {/* Recent Conversations */}
      {/* ---------------------------------------------------------------- */}

      <Box
        sx={{
          flex: 1,
          overflowY: "auto",
          px: collapsed ? 1 : 2.5,
          py: 2,
        }}
      >
        {!collapsed && (
          <Stack
            direction="row"
            spacing={1.25}
            sx={{
              alignItems: "center",
              px: 1,
              mb: 2,
            }}
          >
            <AccessTime
              sx={{
                fontSize: 22,
                color: "text.secondary",
              }}
            />

            <Typography
              variant="body2"
              sx={{
                fontWeight: 600,
                color: "text.secondary",
              }}
            >
              Recent Conversations
            </Typography>
          </Stack>
        )}

        {conversationId ? (
          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              gap: 1.25,
              px: 1.5,
              py: 1.25,
              borderRadius: 2,
              bgcolor: "action.selected",
            }}
          >
            <ChatBubbleOutlined fontSize="small" color="primary" />

            {!collapsed && (
              <Typography
                variant="body2"
                noWrap
                sx={{
                  fontWeight: 500,
                }}
              >
                Current conversation
              </Typography>
            )}
          </Box>
        ) : (
          !collapsed && (
            <Stack
              spacing={1}
              sx={{
                alignItems: "center",
                textAlign: "center",
                px: 2,
                pt: 8,
              }}
            >
              {/* Empty state icon */}
              <Box
                sx={{
                  width: 88,
                  height: 88,
                  borderRadius: "50%",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  bgcolor: "primary.50",
                  color: "primary.main",
                  mb: 1,
                }}
              >
                <ChatBubbleOutlined
                  sx={{
                    fontSize: 42,
                  }}
                />
              </Box>

              <Typography
                variant="h6"
                sx={{
                  fontWeight: 600,
                  color: "text.primary",
                }}
              >
                No conversations yet
              </Typography>

              <Typography
                variant="body2"
                color="text.secondary"
                sx={{
                  maxWidth: 210,
                  lineHeight: 1.6,
                }}
              >
                Upload a document and start asking questions.
              </Typography>
            </Stack>
          )
        )}
      </Box>

      {/* ---------------------------------------------------------------- */}
      {/* Footer */}
      {/* ---------------------------------------------------------------- */}

      <Divider />

      <Box
        sx={{
          px: collapsed ? 1.5 : 3,
          py: 2.5,
        }}
      >
        {collapsed ? (
          <Box
            sx={{
              width: 36,
              height: 36,
              mx: "auto",
              borderRadius: "50%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              bgcolor: "primary.50",
              color: "primary.main",
            }}
          >
            <ChatBubbleOutlined fontSize="small" />
          </Box>
        ) : (
          <Stack
            direction="row"
            spacing={1.25}
            sx={{
              alignItems: "center",
            }}
          >
            {/* Status indicator */}
            <Box
              sx={{
                width: 38,
                height: 38,
                borderRadius: 2,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                bgcolor: "primary.50",
                color: "primary.main",
              }}
            >
              <ChatBubbleOutlined fontSize="small" />
            </Box>

            <Stack spacing={0.25}>
              <Stack
                direction="row"
                spacing={0.75}
                sx={{
                  alignItems: "center",
                }}
              >
                <Box
                  sx={{
                    width: 8,
                    height: 8,
                    borderRadius: "50%",
                    bgcolor: "success.main",
                  }}
                />

                <Typography
                  variant="body2"
                  sx={{
                    fontWeight: 600,
                  }}
                >
                  Document <br />
                  Knowledge Assistant
                </Typography>
              </Stack>

              <Typography variant="caption" color="text.secondary">
                Powered by AI
              </Typography>
            </Stack>
          </Stack>
        )}
      </Box>
    </Box>
  );
}
