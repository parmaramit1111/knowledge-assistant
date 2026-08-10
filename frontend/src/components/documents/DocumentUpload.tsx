import { useRef, useState } from "react";

import { Alert, Box, Button, CircularProgress, Paper, Stack, Typography } from "@mui/material";

import { CloudUploadOutlined, DescriptionOutlined, PictureAsPdfOutlined } from "@mui/icons-material";

interface DocumentUploadProps {
  uploading: boolean;
  error: string | null;
  successMessage?: string | null;
  onUpload: (file: File) => Promise<void>;
}

const ACCEPTED_FILE_TYPE = "application/pdf";

export default function DocumentUpload({ uploading, error, successMessage, onUpload }: DocumentUploadProps) {
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const [dragging, setDragging] = useState(false);

  const handleFile = async (file: File | undefined): Promise<void> => {
    if (!file || uploading) {
      return;
    }

    if (file.type !== ACCEPTED_FILE_TYPE) {
      return;
    }

    await onUpload(file);
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    const file = event.target.files?.[0];

    void handleFile(file);

    event.target.value = "";
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>): void => {
    event.preventDefault();

    setDragging(false);

    const file = event.dataTransfer.files?.[0];

    void handleFile(file);
  };

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>): void => {
    event.preventDefault();

    if (!uploading) {
      setDragging(true);
    }
  };

  const handleDragLeave = (): void => {
    setDragging(false);
  };

  const handleSelectFile = (): void => {
    if (!uploading) {
      fileInputRef.current?.click();
    }
  };

  return (
    <Stack
      spacing={3}
      sx={{
        width: "100%",
        maxWidth: 900,
        mx: "auto",
      }}
    >
      {/* ================================================================ */}
      {/* Upload Card */}
      {/* ================================================================ */}

      <Paper
        elevation={0}
        sx={{
          p: {
            xs: 2,
            sm: 3,
          },
          borderRadius: 4,
          bgcolor: "background.paper",
          border: 1,
          borderColor: "divider",
        }}
      >
        {/* ============================================================ */}
        {/* Drop Zone */}
        {/* ============================================================ */}

        <Box
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onClick={handleSelectFile}
          sx={{
            minHeight: 470,
            px: {
              xs: 2,
              sm: 4,
            },
            py: {
              xs: 4,
              sm: 6,
            },
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            border: "1.5px dashed",
            borderColor: dragging ? "primary.main" : "primary.100",
            borderRadius: 3,
            cursor: uploading ? "default" : "pointer",
            bgcolor: dragging ? "primary.50" : "background.paper",
            transition: "all 0.2s ease",
            "&:hover": {
              borderColor: uploading ? "primary.100" : "primary.light",
            },
          }}
        >
          <Stack
            spacing={3}
            sx={{
              alignItems: "center",
              textAlign: "center",
              maxWidth: 650,
            }}
          >
            {/* ======================================================== */}
            {/* Upload Illustration */}
            {/* ======================================================== */}

            <Box
              sx={{
                position: "relative",
                width: 150,
                height: 120,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              {/* Soft background */}
              <Box
                sx={{
                  position: "absolute",
                  width: 130,
                  height: 130,
                  borderRadius: "50%",
                  bgcolor: "primary.50",
                }}
              />

              {/* PDF document */}
              <Box
                sx={{
                  position: "relative",
                  width: 68,
                  height: 82,
                  borderRadius: 2,
                  bgcolor: "background.paper",
                  border: 3,
                  borderColor: "primary.light",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  boxShadow: 2,
                  transform: "translateX(-18px)",
                }}
              >
                <PictureAsPdfOutlined
                  sx={{
                    fontSize: 42,
                    color: "primary.main",
                  }}
                />

                {/* PDF badge */}
                <Box
                  sx={{
                    position: "absolute",
                    right: -20,
                    top: 28,
                    px: 1,
                    py: 0.35,
                    borderRadius: 1,
                    bgcolor: "error.main",
                    color: "common.white",
                    fontSize: 11,
                    fontWeight: 700,
                    letterSpacing: 0.3,
                  }}
                >
                  PDF
                </Box>
              </Box>

              {/* Cloud */}
              <Box
                sx={{
                  position: "absolute",
                  right: 15,
                  bottom: 12,
                  width: 70,
                  height: 55,
                  borderRadius: 4,
                  bgcolor: "primary.main",
                  color: "common.white",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  boxShadow: 3,
                }}
              >
                <CloudUploadOutlined
                  sx={{
                    fontSize: 38,
                  }}
                />
              </Box>
            </Box>

            {/* ======================================================== */}
            {/* Heading */}
            {/* ======================================================== */}

            <Box>
              <Typography
                variant="h4"
                sx={{
                  fontWeight: 700,
                  color: "text.primary",
                  mb: 1,
                }}
              >
                Upload your PDF
              </Typography>

              <Typography
                variant="body1"
                color="text.secondary"
                sx={{
                  fontSize: 17,
                }}
              >
                Drag and drop your document here, or select a file from your computer.
              </Typography>
            </Box>

            {/* ======================================================== */}
            {/* Select Button */}
            {/* ======================================================== */}

            <Button
              variant="contained"
              size="large"
              startIcon={uploading ? <CircularProgress size={22} color="inherit" /> : <CloudUploadOutlined />}
              disabled={uploading}
              onClick={(event) => {
                event.stopPropagation();
                handleSelectFile();
              }}
              sx={{
                minWidth: 240,
                minHeight: 60,
                px: 4,
                borderRadius: 2.5,
                fontSize: 17,
                fontWeight: 600,
                textTransform: "none",
                boxShadow: "none",
                background: "linear-gradient(135deg, #2979ff 0%, #1565f0 100%)",
                "&:hover": {
                  boxShadow: "none",
                  background: "linear-gradient(135deg, #1565f0 0%, #0d47c7 100%)",
                },
              }}
            >
              {uploading ? "Uploading..." : "Select PDF"}
            </Button>

            {/* ======================================================== */}
            {/* Supported Format */}
            {/* ======================================================== */}

            <Stack
              direction="row"
              spacing={1}
              sx={{
                alignItems: "center",
                color: "text.secondary",
              }}
            >
              <DescriptionOutlined fontSize="small" />

              <Typography variant="body2">Supported format: PDF</Typography>
            </Stack>
          </Stack>
        </Box>
      </Paper>

      {/* ================================================================ */}
      {/* Success Message */}
      {/* ================================================================ */}

      {successMessage && (
        <Alert
          severity="success"
          icon={false}
          sx={{
            borderRadius: 3,
            px: 2.5,
            py: 1.5,
            bgcolor: "success.50",
            border: 1,
            borderColor: "success.100",
          }}
        >
          <Stack
            direction="row"
            spacing={2}
            sx={{
              width: "100%",
              alignItems: "center",
            }}
          >
            {/* Success Icon */}
            <Box
              sx={{
                width: 42,
                height: 42,
                flexShrink: 0,
                borderRadius: "50%",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                bgcolor: "success.main",
                color: "common.white",
                fontSize: 22,
                fontWeight: 700,
              }}
            >
              ✓
            </Box>

            <Box sx={{ flex: 1 }}>
              <Typography
                variant="body1"
                sx={{
                  fontWeight: 700,
                  color: "success.dark",
                }}
              >
                Document uploaded successfully.
              </Typography>

              <Typography variant="body2" color="text.secondary">
                Your document has been received and is being processed.
              </Typography>
            </Box>

            {/* <Button
              variant="text"
              sx={{
                fontWeight: 600,
                textTransform: "none",
                whiteSpace: "nowrap",
              }}
            >
              View Documents →
            </Button> */}
          </Stack>
        </Alert>
      )}

      {/* ================================================================ */}
      {/* Error */}
      {/* ================================================================ */}

      {error && (
        <Alert
          severity="error"
          sx={{
            borderRadius: 3,
          }}
        >
          {error}
        </Alert>
      )}

      {/* ================================================================ */}
      {/* Hidden File Input */}
      {/* ================================================================ */}

      <input ref={fileInputRef} type="file" accept={ACCEPTED_FILE_TYPE} hidden onChange={handleFileChange} />
    </Stack>
  );
}
