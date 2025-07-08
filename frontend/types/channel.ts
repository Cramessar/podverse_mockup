
export interface Channel {
    id: number;
    id_text: string;
    slug: string;
    feed_id: number;
    podcast_index_id?: number;
    podcast_guid: string;
    title: string;
    sortable_title: string;
    medium_id: number;
    has_podcast_idex_value: boolean;
    has_value_time_splits: boolean
    category: Category[];
    medium: Medium[];
}

export interface Category {
    id: number;
    parent_id?: number;
    display_name: string;
    slug: string;
    mapping_key: string;
}

export interface Medium {
    id: number;
    value: string;
}