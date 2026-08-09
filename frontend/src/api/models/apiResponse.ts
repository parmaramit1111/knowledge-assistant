export interface ApiResponse<T> {
  code: string;
  success: boolean;
  message: string;
  result: T;
  total_records: number | null;
  request_id: string;
}
