export interface FeedLog {
  id: number;
  feed_id: number;
  message?: string;
  created_at?: string;
}

export interface Feed {
  id: number;
  feed_flag_status_id: number;
  url: string;
  is_parsing: boolean;
  parsing_priority: number;
  last_parsed_file_hash: string;
  container_id: string;
  created_at: string;
  updated_at: string;
  FeedFlagStatus?: FeedFlagStatus[];
  logs?: FeedLog[];
  recent_logs?: RecentLog[];
}

export interface FeedFlagStatus {
  id: number;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface RecentLog {
  id: number;
  feed_id: number;
  last_finished_parse_time?: string;
  last_good_http_status_time?: string;
  last_http_status?: number;
  message: string;
  parse_errors?: number;
}