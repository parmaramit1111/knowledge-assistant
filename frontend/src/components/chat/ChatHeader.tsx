import { Menu, MoreVert } from "@mui/icons-material";
import { AppBar, IconButton, Toolbar, Typography } from "@mui/material";

interface ChatHeaderProps {
  onMenuClick: () => void;
  sidebarOpen: boolean;
}

export default function ChatHeader({ onMenuClick, sidebarOpen }: ChatHeaderProps) {
  return (
    <AppBar
      position="static"
      color="inherit"
      elevation={0}
      sx={{
        borderBottom: 1,
        borderColor: "divider",
        bgcolor: "background.paper",
      }}
    >
      <Toolbar sx={{ minHeight: 64 }}>
        {/* {!sidebarOpen && (
          <IconButton edge="start" onClick={onMenuClick} aria-label="Open sidebar" sx={{ mr: 1 }}>
            <Menu />
          </IconButton>
        )} */}

        <Typography variant="h6" color="text.primary" sx={{ flex: 1, fontWeight: 700 }}>
          Knowledge Assistant
        </Typography>

        <IconButton aria-label="More options">
          <MoreVert />
        </IconButton>
      </Toolbar>
    </AppBar>
  );
}
