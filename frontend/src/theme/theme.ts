import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    mode: "light",

    primary: {
      main: "#2563EB",
      light: "#60A5FA",
      dark: "#1D4ED8",
      contrastText: "#FFFFFF",
    },

    secondary: {
      main: "#6366F1",
      light: "#818CF8",
      dark: "#4F46E5",
      contrastText: "#FFFFFF",
    },

    background: {
      default: "#F8FAFC",
      paper: "#FFFFFF",
    },

    text: {
      primary: "#111827",
      secondary: "#6B7280",
    },

    divider: "#E5E7EB",

    error: {
      main: "#DC2626",
    },

    success: {
      main: "#16A34A",
    },

    warning: {
      main: "#D97706",
    },
  },

  typography: {
    fontFamily: ["Inter", "-apple-system", "BlinkMacSystemFont", '"Segoe UI"', "Roboto", '"Helvetica Neue"', "Arial", "sans-serif"].join(","),

    h1: {
      fontSize: "2rem",
      fontWeight: 700,
      lineHeight: 1.2,
    },

    h2: {
      fontSize: "1.5rem",
      fontWeight: 700,
      lineHeight: 1.3,
    },

    h3: {
      fontSize: "1.25rem",
      fontWeight: 600,
      lineHeight: 1.4,
    },

    body1: {
      fontSize: "0.95rem",
      lineHeight: 1.6,
    },

    body2: {
      fontSize: "0.875rem",
      lineHeight: 1.5,
    },

    button: {
      textTransform: "none",
      fontWeight: 600,
    },
  },

  shape: {
    borderRadius: 10,
  },

  spacing: 8,

  components: {
    MuiButton: {
      defaultProps: {
        disableElevation: true,
      },

      styleOverrides: {
        root: {
          borderRadius: 8,
        },
      },
    },

    MuiTextField: {
      defaultProps: {
        variant: "outlined",
      },
    },

    MuiOutlinedInput: {
      styleOverrides: {
        root: {
          borderRadius: 10,

          "&:hover .MuiOutlinedInput-notchedOutline": {
            borderColor: "#94A3B8",
          },

          "&.Mui-focused .MuiOutlinedInput-notchedOutline": {
            borderWidth: 1,
          },
        },
      },
    },

    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: "none",
        },
      },
    },

    MuiCard: {
      styleOverrides: {
        root: {
          border: "1px solid #E5E7EB",
          boxShadow: "0 1px 2px rgba(0, 0, 0, 0.04)",
        },
      },
    },
  },
});

export default theme;
