import { Box } from "@mui/material";

interface BrandLogoProps {
  collapsed?: boolean;
  height?: number;
}

export function BrandLogo({ collapsed = false, height }: BrandLogoProps) {
  const logoSrc = collapsed ? "/assets/logo/knowledge-assistant-icon.png" : "/assets/logo/knowledge-assistant-logo.png";

  return (
    <Box
      component="img"
      src={logoSrc}
      alt="Knowledge Assistant"
      sx={{
        height: height ?? (collapsed ? 42 : 52),
        width: "auto",
        maxWidth: collapsed ? 48 : 190,
        objectFit: "contain",
        display: "block",
      }}
    />
  );
}
