### **Table: `category`**
| Field | Type |
|-------|------|
| id | SERIAL PRIMARY |
| parent_id | INTEGER REFERENCES |
| display_name | varchar_normal NOT |
| slug | varchar_normal NOT |
| mapping_key | varchar_normal NOT |

---

### **Table: `medium`**
| Field | Type |
|-------|------|
| id | SERIAL PRIMARY |
| value | TEXT UNIQUE |

---

### **Table: `feed_flag_status`**
| Field | Type |
|-------|------|
| id | SERIAL PRIMARY |
| status | TEXT UNIQUE |
| created_at | server_time_with_default |
| updated_at | server_time_with_default |

---

### **Table: `feed`**
| Field | Type |
|-------|------|
| id | SERIAL PRIMARY |
| url | varchar_url UNIQUE |
| feed_flag_status_id | INTEGER NOT |
| is_parsing | BOOLEAN DEFAULT |
| parsing_priority | INTEGER DEFAULT |
| last_parsed_file_hash | varchar_md5 |
| container_id | VARCHAR(12) |
| created_at | server_time_with_default |
| updated_at | server_time_with_default |

---

### **Table: `feed_log`**
| Field | Type |
|-------|------|
| id | SERIAL PRIMARY |
| feed_id | INTEGER NOT |
| last_http_status | INTEGER |
| last_good_http_status_time | server_time |
| last_finished_parse_time | server_time |
| parse_errors | INTEGER DEFAULT |

---

### **Table: `channel`**
| Field | Type |
|-------|------|
| id | SERIAL PRIMARY |
| id_text | short_id_v2 UNIQUE |
| slug | varchar_slug |
| feed_id | INTEGER NOT |
| podcast_index_id | INTEGER UNIQUE |
| podcast_guid | UUID UNIQUE |
| title | varchar_normal |
| sortable_title | varchar_short |
| medium_id | INTEGER REFERENCES |
| has_podcast_index_value | BOOLEAN DEFAULT |
| has_value_time_splits | BOOLEAN DEFAULT |

---

### **Table: `channel_category`**
| Field | Type |
|-------|------|
| id | SERIAL PRIMARY |
| channel_id | INTEGER NOT |
| category_id | INTEGER NOT |

---

### **Table: `item_flag_status`**
| Field | Type |
|-------|------|
| id | SERIAL PRIMARY |
| status | TEXT UNIQUE |
| created_at | server_time_with_default |
| updated_at | server_time_with_default |

---

### **Table: `item`**
| Field | Type |
|-------|------|
| id | SERIAL PRIMARY |
| id_text | short_id_v2 UNIQUE |
| slug | varchar_slug |
| channel_id | INTEGER NOT |
| guid | varchar_uri |
| guid_enclosure_url | varchar_url |
| pub_date | TIMESTAMPTZ |
| title | varchar_normal |
| item_flag_status_id | INTEGER NOT |

---

### **Table: `sharable_status`**
| Field | Type |
|-------|------|
| id | SERIAL PRIMARY |
| status | TEXT UNIQUE |

---

### **Table: `account`**
| Field | Type |
|-------|------|
| id | SERIAL PRIMARY |
| id_text | short_id_v2 UNIQUE |
| verified | BOOLEAN DEFAULT |
| sharable_status_id | INTEGER NOT |

---

### **Table: `stats_track_account_guid`**
| Field | Type |
|-------|------|
| id | SERIAL PRIMARY |
| account_id | INT NOT |
| account_guid | UUID NOT |
| updated_at | server_time_with_default NOT |

---

### **Table: `stats_track_event_channel`**
| Field | Type |
|-------|------|
| id | SERIAL PRIMARY |
| account_guid | UUID NOT |
| channel_id | INT NOT |
| created_at | server_time_with_default NOT |

---

### **Table: `stats_aggregated_channel`**
| Field | Type |
|-------|------|
| id | SERIAL PRIMARY |
| channel_id | INT NOT |
| day_current_count | INT NOT |
| day_1_count | INT NOT |
| day_2_count | INT NOT |
| day_3_count | INT NOT |
| day_4_count | INT NOT |
| day_5_count | INT NOT |
| day_6_count | INT NOT |
| day_7_count | INT NOT |
| day_8_count | INT NOT |
| week_current_count | INT NOT |
| week_1_count | INT NOT |
| week_2_count | INT NOT |
| week_3_count | INT NOT |
| week_4_count | INT NOT |
| month_current_count | INT NOT |
| month_1_count | INT NOT |
| all_time_count | INT NOT |

---

### **Table: `stats_track_event_item`**
| Field | Type |
|-------|------|
| id | SERIAL PRIMARY |
| account_guid | UUID NOT |
| item_id | INT NOT |
| created_at | server_time_with_default NOT |

---

### **Table: `stats_aggregated_item`**
| Field | Type |
|-------|------|
| id | SERIAL PRIMARY |
| item_id | INT NOT |
| day_current_count | INT NOT |
| day_1_count | INT NOT |
| day_2_count | INT NOT |
| day_3_count | INT NOT |
| day_4_count | INT NOT |
| day_5_count | INT NOT |
| day_6_count | INT NOT |
| day_7_count | INT NOT |
| day_8_count | INT NOT |
| week_current_count | INT NOT |
| week_1_count | INT NOT |
| week_2_count | INT NOT |
| week_3_count | INT NOT |
| week_4_count | INT NOT |
| month_current_count | INT NOT |
| month_1_count | INT NOT |
| all_time_count | INT NOT |

### **Table: `export_logs`**
| Field | Type |
|-------|------|
| id | SERIAL PRIMARY |
| admin_email | varchar_normal NOT |
| export_type | TEXT NOT |
| filters | JSONB |
| status | TEXT NOT |
| file_path | TEXT |
| created_at | server_time_with_default NOT |
| completed_at | server_time |
| error_message | TEXT |
| format | TEXT NOT |

---

