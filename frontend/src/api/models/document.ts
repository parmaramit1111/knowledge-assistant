// export interface DocumentUploadResponse {
//   id: string;
//   file_name: string;
//   status: string;
// }

export interface DocumentUploadResponse {
  id: string;
  filename: string;
  contentType: string;
  size: number;
  status: string;
  createdAt: string;
  message: string;
}
