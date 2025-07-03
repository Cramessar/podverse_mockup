export interface FeedLog {
  time: string;
  message: string;
}

export interface Feed {
  id: number;
  url: string;
  feed_flag_status_id: number;
  is_parsing: boolean;
  parsing_priority: number;
  last_parsed_file_hash: string;
  container_id: string;
  created_at: string;
  updated_at: string;
  logs?: FeedLog[];
}