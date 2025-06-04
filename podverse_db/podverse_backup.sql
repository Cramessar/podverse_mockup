--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

-- Started on 2025-06-04 18:24:09

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 1082 (class 1247 OID 24844)
-- Name: list_position; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.list_position AS numeric(22,21);


ALTER DOMAIN public.list_position OWNER TO postgres;

--
-- TOC entry 1079 (class 1247 OID 24842)
-- Name: media_player_time; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.media_player_time AS numeric(10,2);


ALTER DOMAIN public.media_player_time OWNER TO postgres;

--
-- TOC entry 1085 (class 1247 OID 24846)
-- Name: numeric_20_11; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.numeric_20_11 AS numeric(20,11);


ALTER DOMAIN public.numeric_20_11 OWNER TO postgres;

--
-- TOC entry 1073 (class 1247 OID 24838)
-- Name: server_time; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.server_time AS timestamp without time zone;


ALTER DOMAIN public.server_time OWNER TO postgres;

--
-- TOC entry 1076 (class 1247 OID 24840)
-- Name: server_time_with_default; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.server_time_with_default AS timestamp without time zone DEFAULT now();


ALTER DOMAIN public.server_time_with_default OWNER TO postgres;

--
-- TOC entry 1032 (class 1247 OID 24810)
-- Name: short_id_v2; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.short_id_v2 AS character varying(15);


ALTER DOMAIN public.short_id_v2 OWNER TO postgres;

--
-- TOC entry 1044 (class 1247 OID 24818)
-- Name: varchar_email; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.varchar_email AS character varying(255)
	CONSTRAINT varchar_email_check CHECK (((VALUE)::text ~ '^.+@.+\..+$'::text));


ALTER DOMAIN public.varchar_email OWNER TO postgres;

--
-- TOC entry 1048 (class 1247 OID 24821)
-- Name: varchar_fcm_token; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.varchar_fcm_token AS character varying(255);


ALTER DOMAIN public.varchar_fcm_token OWNER TO postgres;

--
-- TOC entry 1051 (class 1247 OID 24823)
-- Name: varchar_fqdn; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.varchar_fqdn AS character varying(253);


ALTER DOMAIN public.varchar_fqdn OWNER TO postgres;

--
-- TOC entry 1054 (class 1247 OID 24825)
-- Name: varchar_guid; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.varchar_guid AS character varying(36);


ALTER DOMAIN public.varchar_guid OWNER TO postgres;

--
-- TOC entry 1041 (class 1247 OID 24816)
-- Name: varchar_long; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.varchar_long AS character varying(2500);


ALTER DOMAIN public.varchar_long OWNER TO postgres;

--
-- TOC entry 1057 (class 1247 OID 24827)
-- Name: varchar_md5; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.varchar_md5 AS character varying(32);


ALTER DOMAIN public.varchar_md5 OWNER TO postgres;

--
-- TOC entry 1038 (class 1247 OID 24814)
-- Name: varchar_normal; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.varchar_normal AS character varying(255);


ALTER DOMAIN public.varchar_normal OWNER TO postgres;

--
-- TOC entry 1060 (class 1247 OID 24829)
-- Name: varchar_password; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.varchar_password AS character varying(60);


ALTER DOMAIN public.varchar_password OWNER TO postgres;

--
-- TOC entry 1035 (class 1247 OID 24812)
-- Name: varchar_short; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.varchar_short AS character varying(50);


ALTER DOMAIN public.varchar_short OWNER TO postgres;

--
-- TOC entry 1063 (class 1247 OID 24831)
-- Name: varchar_slug; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.varchar_slug AS character varying(100);


ALTER DOMAIN public.varchar_slug OWNER TO postgres;

--
-- TOC entry 1066 (class 1247 OID 24833)
-- Name: varchar_uri; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.varchar_uri AS character varying(2083);


ALTER DOMAIN public.varchar_uri OWNER TO postgres;

--
-- TOC entry 1069 (class 1247 OID 24835)
-- Name: varchar_url; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.varchar_url AS character varying(2083)
	CONSTRAINT varchar_url_check CHECK (((VALUE)::text ~ '^https?://|^http?://'::text));


ALTER DOMAIN public.varchar_url OWNER TO postgres;

--
-- TOC entry 403 (class 1255 OID 26172)
-- Name: delete_playlist_resource(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.delete_playlist_resource() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    -- Custom logic for deleting related resources can be added here if needed
    RETURN OLD;
END;
$$;


ALTER FUNCTION public.delete_playlist_resource() OWNER TO postgres;

--
-- TOC entry 402 (class 1255 OID 24847)
-- Name: set_updated_at_field(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.set_updated_at_field() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at := NOW();
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.set_updated_at_field() OWNER TO postgres;

SET default_table_access_method = heap;

--
-- TOC entry 340 (class 1259 OID 25904)
-- Name: account; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account (
    id integer NOT NULL,
    id_text public.short_id_v2 NOT NULL,
    verified boolean DEFAULT false,
    sharable_status_id integer NOT NULL
);


ALTER TABLE public.account OWNER TO postgres;

--
-- TOC entry 356 (class 1259 OID 26042)
-- Name: account_admin_roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account_admin_roles (
    id integer NOT NULL,
    account_id integer NOT NULL,
    dev_admin boolean DEFAULT false,
    podping_admin boolean DEFAULT false
);


ALTER TABLE public.account_admin_roles OWNER TO postgres;

--
-- TOC entry 355 (class 1259 OID 26041)
-- Name: account_admin_roles_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.account_admin_roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.account_admin_roles_id_seq OWNER TO postgres;

--
-- TOC entry 6479 (class 0 OID 0)
-- Dependencies: 355
-- Name: account_admin_roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.account_admin_roles_id_seq OWNED BY public.account_admin_roles.id;


--
-- TOC entry 377 (class 1259 OID 26385)
-- Name: account_app_store_purchase; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account_app_store_purchase (
    account_id integer NOT NULL,
    transaction_id character varying NOT NULL,
    cancellation_date character varying,
    cancellation_date_ms character varying,
    cancellation_date_pst character varying,
    cancellation_reason character varying,
    expires_date character varying,
    expires_date_ms character varying,
    expires_date_pst character varying,
    is_in_intro_offer_period boolean,
    is_trial_period boolean,
    original_purchase_date character varying,
    original_purchase_date_ms character varying,
    original_purchase_date_pst character varying,
    original_transaction_id character varying,
    product_id character varying,
    promotional_offer_id character varying,
    purchase_date character varying,
    purchase_date_ms character varying,
    purchase_date_pst character varying,
    quantity integer,
    web_order_line_item_id character varying
);


ALTER TABLE public.account_app_store_purchase OWNER TO postgres;

--
-- TOC entry 342 (class 1259 OID 25922)
-- Name: account_credentials; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account_credentials (
    id integer NOT NULL,
    account_id integer NOT NULL,
    email public.varchar_email NOT NULL,
    password public.varchar_password NOT NULL
);


ALTER TABLE public.account_credentials OWNER TO postgres;

--
-- TOC entry 341 (class 1259 OID 25921)
-- Name: account_credentials_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.account_credentials_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.account_credentials_id_seq OWNER TO postgres;

--
-- TOC entry 6483 (class 0 OID 0)
-- Dependencies: 341
-- Name: account_credentials_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.account_credentials_id_seq OWNED BY public.account_credentials.id;


--
-- TOC entry 350 (class 1259 OID 25992)
-- Name: account_email_change_verification; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account_email_change_verification (
    id integer NOT NULL,
    account_id integer NOT NULL,
    verification_token public.varchar_guid,
    verification_token_expires_at timestamp without time zone,
    pending_email_address public.varchar_email
);


ALTER TABLE public.account_email_change_verification OWNER TO postgres;

--
-- TOC entry 349 (class 1259 OID 25991)
-- Name: account_email_change_verification_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.account_email_change_verification_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.account_email_change_verification_id_seq OWNER TO postgres;

--
-- TOC entry 6486 (class 0 OID 0)
-- Dependencies: 349
-- Name: account_email_change_verification_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.account_email_change_verification_id_seq OWNED BY public.account_email_change_verification.id;


--
-- TOC entry 375 (class 1259 OID 26355)
-- Name: account_fcm_device; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account_fcm_device (
    id integer NOT NULL,
    fcm_token public.varchar_fcm_token NOT NULL,
    account_id integer NOT NULL
);


ALTER TABLE public.account_fcm_device OWNER TO postgres;

--
-- TOC entry 374 (class 1259 OID 26354)
-- Name: account_fcm_device_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.account_fcm_device_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.account_fcm_device_id_seq OWNER TO postgres;

--
-- TOC entry 6489 (class 0 OID 0)
-- Dependencies: 374
-- Name: account_fcm_device_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.account_fcm_device_id_seq OWNED BY public.account_fcm_device.id;


--
-- TOC entry 367 (class 1259 OID 26255)
-- Name: account_following_account; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account_following_account (
    account_id integer NOT NULL,
    following_account_id integer NOT NULL
);


ALTER TABLE public.account_following_account OWNER TO postgres;

--
-- TOC entry 370 (class 1259 OID 26306)
-- Name: account_following_add_by_rss_channel; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account_following_add_by_rss_channel (
    account_id integer NOT NULL,
    feed_url public.varchar_url NOT NULL,
    title public.varchar_normal,
    image_url public.varchar_url
);


ALTER TABLE public.account_following_add_by_rss_channel OWNER TO postgres;

--
-- TOC entry 368 (class 1259 OID 26272)
-- Name: account_following_channel; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account_following_channel (
    account_id integer NOT NULL,
    channel_id integer NOT NULL
);


ALTER TABLE public.account_following_channel OWNER TO postgres;

--
-- TOC entry 369 (class 1259 OID 26289)
-- Name: account_following_playlist; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account_following_playlist (
    account_id integer NOT NULL,
    playlist_id integer NOT NULL
);


ALTER TABLE public.account_following_playlist OWNER TO postgres;

--
-- TOC entry 378 (class 1259 OID 26398)
-- Name: account_google_play_purchase; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account_google_play_purchase (
    account_id integer NOT NULL,
    transaction_id character varying NOT NULL,
    acknowledgement_state integer,
    consumption_state integer,
    developer_payload character varying,
    kind character varying,
    product_id character varying NOT NULL,
    purchase_time_millis character varying,
    purchase_state integer,
    purchase_token character varying NOT NULL
);


ALTER TABLE public.account_google_play_purchase OWNER TO postgres;

--
-- TOC entry 339 (class 1259 OID 25903)
-- Name: account_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.account_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.account_id_seq OWNER TO postgres;

--
-- TOC entry 6496 (class 0 OID 0)
-- Dependencies: 339
-- Name: account_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.account_id_seq OWNED BY public.account.id;


--
-- TOC entry 352 (class 1259 OID 26009)
-- Name: account_membership; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account_membership (
    id integer NOT NULL,
    tier text,
    CONSTRAINT account_membership_tier_check CHECK ((tier = ANY (ARRAY['trial'::text, 'basic'::text])))
);


ALTER TABLE public.account_membership OWNER TO postgres;

--
-- TOC entry 351 (class 1259 OID 26008)
-- Name: account_membership_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.account_membership_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.account_membership_id_seq OWNER TO postgres;

--
-- TOC entry 6499 (class 0 OID 0)
-- Dependencies: 351
-- Name: account_membership_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.account_membership_id_seq OWNED BY public.account_membership.id;


--
-- TOC entry 354 (class 1259 OID 26021)
-- Name: account_membership_status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account_membership_status (
    id integer NOT NULL,
    account_id integer NOT NULL,
    account_membership_id integer NOT NULL,
    membership_expires_at timestamp without time zone
);


ALTER TABLE public.account_membership_status OWNER TO postgres;

--
-- TOC entry 353 (class 1259 OID 26020)
-- Name: account_membership_status_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.account_membership_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.account_membership_status_id_seq OWNER TO postgres;

--
-- TOC entry 6502 (class 0 OID 0)
-- Dependencies: 353
-- Name: account_membership_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.account_membership_status_id_seq OWNED BY public.account_membership_status.id;


--
-- TOC entry 371 (class 1259 OID 26319)
-- Name: account_notification_channel; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account_notification_channel (
    channel_id integer NOT NULL,
    account_id integer NOT NULL
);


ALTER TABLE public.account_notification_channel OWNER TO postgres;

--
-- TOC entry 376 (class 1259 OID 26372)
-- Name: account_paypal_order; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account_paypal_order (
    account_id integer NOT NULL,
    payment_id character varying NOT NULL,
    state character varying
);


ALTER TABLE public.account_paypal_order OWNER TO postgres;

--
-- TOC entry 344 (class 1259 OID 25941)
-- Name: account_profile; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account_profile (
    id integer NOT NULL,
    account_id integer NOT NULL,
    display_name public.varchar_normal,
    bio public.varchar_long
);


ALTER TABLE public.account_profile OWNER TO postgres;

--
-- TOC entry 343 (class 1259 OID 25940)
-- Name: account_profile_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.account_profile_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.account_profile_id_seq OWNER TO postgres;

--
-- TOC entry 6507 (class 0 OID 0)
-- Dependencies: 343
-- Name: account_profile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.account_profile_id_seq OWNED BY public.account_profile.id;


--
-- TOC entry 346 (class 1259 OID 25958)
-- Name: account_reset_password; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account_reset_password (
    id integer NOT NULL,
    account_id integer NOT NULL,
    reset_token public.varchar_guid,
    reset_token_expires_at timestamp without time zone
);


ALTER TABLE public.account_reset_password OWNER TO postgres;

--
-- TOC entry 345 (class 1259 OID 25957)
-- Name: account_reset_password_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.account_reset_password_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.account_reset_password_id_seq OWNER TO postgres;

--
-- TOC entry 6510 (class 0 OID 0)
-- Dependencies: 345
-- Name: account_reset_password_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.account_reset_password_id_seq OWNED BY public.account_reset_password.id;


--
-- TOC entry 373 (class 1259 OID 26337)
-- Name: account_up_device; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account_up_device (
    id integer NOT NULL,
    account_id integer NOT NULL,
    up_endpoint public.varchar_url NOT NULL,
    up_public_key public.varchar_long NOT NULL,
    up_auth_key public.varchar_long NOT NULL
);


ALTER TABLE public.account_up_device OWNER TO postgres;

--
-- TOC entry 372 (class 1259 OID 26336)
-- Name: account_up_device_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.account_up_device_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.account_up_device_id_seq OWNER TO postgres;

--
-- TOC entry 6513 (class 0 OID 0)
-- Dependencies: 372
-- Name: account_up_device_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.account_up_device_id_seq OWNED BY public.account_up_device.id;


--
-- TOC entry 348 (class 1259 OID 25975)
-- Name: account_verification; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account_verification (
    id integer NOT NULL,
    account_id integer NOT NULL,
    verification_token public.varchar_guid,
    verification_token_expires_at timestamp without time zone
);


ALTER TABLE public.account_verification OWNER TO postgres;

--
-- TOC entry 347 (class 1259 OID 25974)
-- Name: account_verification_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.account_verification_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.account_verification_id_seq OWNER TO postgres;

--
-- TOC entry 6516 (class 0 OID 0)
-- Dependencies: 347
-- Name: account_verification_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.account_verification_id_seq OWNED BY public.account_verification.id;


--
-- TOC entry 218 (class 1259 OID 24849)
-- Name: category; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.category (
    id integer NOT NULL,
    parent_id integer,
    display_name public.varchar_normal NOT NULL,
    slug public.varchar_normal NOT NULL,
    mapping_key public.varchar_normal NOT NULL
);


ALTER TABLE public.category OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 24848)
-- Name: category_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.category_id_seq OWNER TO postgres;

--
-- TOC entry 6519 (class 0 OID 0)
-- Dependencies: 217
-- Name: category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.category_id_seq OWNED BY public.category.id;


--
-- TOC entry 228 (class 1259 OID 24925)
-- Name: channel; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.channel (
    id integer NOT NULL,
    id_text public.short_id_v2 NOT NULL,
    slug public.varchar_slug,
    feed_id integer NOT NULL,
    podcast_index_id integer NOT NULL,
    podcast_guid uuid,
    title public.varchar_normal,
    sortable_title public.varchar_short,
    medium_id integer,
    has_podcast_index_value boolean DEFAULT false,
    has_value_time_splits boolean DEFAULT false
);


ALTER TABLE public.channel OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 24970)
-- Name: channel_about; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.channel_about (
    id integer NOT NULL,
    channel_id integer NOT NULL,
    author public.varchar_normal,
    episode_count integer,
    explicit boolean,
    itunes_type_id integer,
    language public.varchar_short,
    last_pub_date public.server_time_with_default,
    website_link_url public.varchar_url
);


ALTER TABLE public.channel_about OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 24969)
-- Name: channel_about_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.channel_about_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.channel_about_id_seq OWNER TO postgres;

--
-- TOC entry 6523 (class 0 OID 0)
-- Dependencies: 231
-- Name: channel_about_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.channel_about_id_seq OWNED BY public.channel_about.id;


--
-- TOC entry 234 (class 1259 OID 24993)
-- Name: channel_category; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.channel_category (
    id integer NOT NULL,
    channel_id integer NOT NULL,
    category_id integer NOT NULL
);


ALTER TABLE public.channel_category OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 24992)
-- Name: channel_category_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.channel_category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.channel_category_id_seq OWNER TO postgres;

--
-- TOC entry 6526 (class 0 OID 0)
-- Dependencies: 233
-- Name: channel_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.channel_category_id_seq OWNED BY public.channel_category.id;


--
-- TOC entry 236 (class 1259 OID 25012)
-- Name: channel_chat; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.channel_chat (
    id integer NOT NULL,
    channel_id integer NOT NULL,
    server public.varchar_fqdn NOT NULL,
    protocol public.varchar_short NOT NULL,
    account_id public.varchar_normal,
    space public.varchar_normal
);


ALTER TABLE public.channel_chat OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 25011)
-- Name: channel_chat_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.channel_chat_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.channel_chat_id_seq OWNER TO postgres;

--
-- TOC entry 6529 (class 0 OID 0)
-- Dependencies: 235
-- Name: channel_chat_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.channel_chat_id_seq OWNED BY public.channel_chat.id;


--
-- TOC entry 238 (class 1259 OID 25029)
-- Name: channel_description; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.channel_description (
    id integer NOT NULL,
    channel_id integer NOT NULL,
    value public.varchar_long NOT NULL
);


ALTER TABLE public.channel_description OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 25028)
-- Name: channel_description_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.channel_description_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.channel_description_id_seq OWNER TO postgres;

--
-- TOC entry 6532 (class 0 OID 0)
-- Dependencies: 237
-- Name: channel_description_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.channel_description_id_seq OWNED BY public.channel_description.id;


--
-- TOC entry 240 (class 1259 OID 25046)
-- Name: channel_funding; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.channel_funding (
    id integer NOT NULL,
    channel_id integer NOT NULL,
    url public.varchar_url NOT NULL,
    title public.varchar_normal
);


ALTER TABLE public.channel_funding OWNER TO postgres;

--
-- TOC entry 239 (class 1259 OID 25045)
-- Name: channel_funding_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.channel_funding_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.channel_funding_id_seq OWNER TO postgres;

--
-- TOC entry 6535 (class 0 OID 0)
-- Dependencies: 239
-- Name: channel_funding_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.channel_funding_id_seq OWNED BY public.channel_funding.id;


--
-- TOC entry 227 (class 1259 OID 24924)
-- Name: channel_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.channel_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.channel_id_seq OWNER TO postgres;

--
-- TOC entry 6537 (class 0 OID 0)
-- Dependencies: 227
-- Name: channel_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.channel_id_seq OWNED BY public.channel.id;


--
-- TOC entry 242 (class 1259 OID 25061)
-- Name: channel_image; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.channel_image (
    id integer NOT NULL,
    channel_id integer NOT NULL,
    url public.varchar_url NOT NULL,
    image_width_size integer,
    is_resized boolean DEFAULT false
);


ALTER TABLE public.channel_image OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 25060)
-- Name: channel_image_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.channel_image_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.channel_image_id_seq OWNER TO postgres;

--
-- TOC entry 6540 (class 0 OID 0)
-- Dependencies: 241
-- Name: channel_image_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.channel_image_id_seq OWNED BY public.channel_image.id;


--
-- TOC entry 244 (class 1259 OID 25077)
-- Name: channel_internal_settings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.channel_internal_settings (
    id integer NOT NULL,
    channel_id integer NOT NULL,
    embed_approved_media_url_paths text
);


ALTER TABLE public.channel_internal_settings OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 25076)
-- Name: channel_internal_settings_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.channel_internal_settings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.channel_internal_settings_id_seq OWNER TO postgres;

--
-- TOC entry 6543 (class 0 OID 0)
-- Dependencies: 243
-- Name: channel_internal_settings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.channel_internal_settings_id_seq OWNED BY public.channel_internal_settings.id;


--
-- TOC entry 230 (class 1259 OID 24958)
-- Name: channel_itunes_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.channel_itunes_type (
    id integer NOT NULL,
    itunes_type text,
    CONSTRAINT channel_itunes_type_itunes_type_check CHECK ((itunes_type = ANY (ARRAY['episodic'::text, 'serial'::text])))
);


ALTER TABLE public.channel_itunes_type OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 24957)
-- Name: channel_itunes_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.channel_itunes_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.channel_itunes_type_id_seq OWNER TO postgres;

--
-- TOC entry 6546 (class 0 OID 0)
-- Dependencies: 229
-- Name: channel_itunes_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.channel_itunes_type_id_seq OWNED BY public.channel_itunes_type.id;


--
-- TOC entry 246 (class 1259 OID 25092)
-- Name: channel_license; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.channel_license (
    id integer NOT NULL,
    channel_id integer NOT NULL,
    identifier public.varchar_normal NOT NULL,
    url public.varchar_url
);


ALTER TABLE public.channel_license OWNER TO postgres;

--
-- TOC entry 245 (class 1259 OID 25091)
-- Name: channel_license_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.channel_license_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.channel_license_id_seq OWNER TO postgres;

--
-- TOC entry 6549 (class 0 OID 0)
-- Dependencies: 245
-- Name: channel_license_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.channel_license_id_seq OWNED BY public.channel_license.id;


--
-- TOC entry 248 (class 1259 OID 25109)
-- Name: channel_location; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.channel_location (
    id integer NOT NULL,
    channel_id integer NOT NULL,
    geo public.varchar_normal,
    osm public.varchar_normal,
    name public.varchar_normal,
    CONSTRAINT channel_location_check CHECK (((geo IS NOT NULL) OR (osm IS NOT NULL)))
);


ALTER TABLE public.channel_location OWNER TO postgres;

--
-- TOC entry 247 (class 1259 OID 25108)
-- Name: channel_location_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.channel_location_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.channel_location_id_seq OWNER TO postgres;

--
-- TOC entry 6552 (class 0 OID 0)
-- Dependencies: 247
-- Name: channel_location_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.channel_location_id_seq OWNED BY public.channel_location.id;


--
-- TOC entry 250 (class 1259 OID 25127)
-- Name: channel_person; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.channel_person (
    id integer NOT NULL,
    channel_id integer NOT NULL,
    name public.varchar_normal NOT NULL,
    role public.varchar_normal,
    person_group public.varchar_normal DEFAULT 'cast'::character varying,
    img public.varchar_url,
    href public.varchar_url
);


ALTER TABLE public.channel_person OWNER TO postgres;

--
-- TOC entry 249 (class 1259 OID 25126)
-- Name: channel_person_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.channel_person_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.channel_person_id_seq OWNER TO postgres;

--
-- TOC entry 6555 (class 0 OID 0)
-- Dependencies: 249
-- Name: channel_person_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.channel_person_id_seq OWNED BY public.channel_person.id;


--
-- TOC entry 252 (class 1259 OID 25143)
-- Name: channel_podroll; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.channel_podroll (
    id integer NOT NULL,
    channel_id integer NOT NULL
);


ALTER TABLE public.channel_podroll OWNER TO postgres;

--
-- TOC entry 251 (class 1259 OID 25142)
-- Name: channel_podroll_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.channel_podroll_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.channel_podroll_id_seq OWNER TO postgres;

--
-- TOC entry 6558 (class 0 OID 0)
-- Dependencies: 251
-- Name: channel_podroll_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.channel_podroll_id_seq OWNED BY public.channel_podroll.id;


--
-- TOC entry 254 (class 1259 OID 25158)
-- Name: channel_podroll_remote_item; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.channel_podroll_remote_item (
    id integer NOT NULL,
    channel_podroll_id integer NOT NULL,
    feed_guid uuid NOT NULL,
    feed_url public.varchar_url,
    item_guid public.varchar_uri,
    title public.varchar_normal,
    medium_id integer
);


ALTER TABLE public.channel_podroll_remote_item OWNER TO postgres;

--
-- TOC entry 253 (class 1259 OID 25157)
-- Name: channel_podroll_remote_item_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.channel_podroll_remote_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.channel_podroll_remote_item_id_seq OWNER TO postgres;

--
-- TOC entry 6561 (class 0 OID 0)
-- Dependencies: 253
-- Name: channel_podroll_remote_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.channel_podroll_remote_item_id_seq OWNED BY public.channel_podroll_remote_item.id;


--
-- TOC entry 256 (class 1259 OID 25182)
-- Name: channel_publisher; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.channel_publisher (
    id integer NOT NULL,
    channel_id integer NOT NULL
);


ALTER TABLE public.channel_publisher OWNER TO postgres;

--
-- TOC entry 255 (class 1259 OID 25181)
-- Name: channel_publisher_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.channel_publisher_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.channel_publisher_id_seq OWNER TO postgres;

--
-- TOC entry 6564 (class 0 OID 0)
-- Dependencies: 255
-- Name: channel_publisher_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.channel_publisher_id_seq OWNED BY public.channel_publisher.id;


--
-- TOC entry 258 (class 1259 OID 25197)
-- Name: channel_publisher_remote_item; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.channel_publisher_remote_item (
    id integer NOT NULL,
    channel_publisher_id integer NOT NULL,
    feed_guid uuid NOT NULL,
    feed_url public.varchar_url,
    item_guid public.varchar_uri,
    title public.varchar_normal,
    medium_id integer
);


ALTER TABLE public.channel_publisher_remote_item OWNER TO postgres;

--
-- TOC entry 257 (class 1259 OID 25196)
-- Name: channel_publisher_remote_item_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.channel_publisher_remote_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.channel_publisher_remote_item_id_seq OWNER TO postgres;

--
-- TOC entry 6567 (class 0 OID 0)
-- Dependencies: 257
-- Name: channel_publisher_remote_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.channel_publisher_remote_item_id_seq OWNED BY public.channel_publisher_remote_item.id;


--
-- TOC entry 260 (class 1259 OID 25223)
-- Name: channel_remote_item; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.channel_remote_item (
    id integer NOT NULL,
    channel_id integer NOT NULL,
    feed_guid uuid NOT NULL,
    feed_url public.varchar_url,
    item_guid public.varchar_uri,
    title public.varchar_normal,
    medium_id integer
);


ALTER TABLE public.channel_remote_item OWNER TO postgres;

--
-- TOC entry 259 (class 1259 OID 25222)
-- Name: channel_remote_item_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.channel_remote_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.channel_remote_item_id_seq OWNER TO postgres;

--
-- TOC entry 6570 (class 0 OID 0)
-- Dependencies: 259
-- Name: channel_remote_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.channel_remote_item_id_seq OWNED BY public.channel_remote_item.id;


--
-- TOC entry 262 (class 1259 OID 25247)
-- Name: channel_season; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.channel_season (
    id integer NOT NULL,
    channel_id integer NOT NULL,
    number integer NOT NULL,
    name public.varchar_normal
);


ALTER TABLE public.channel_season OWNER TO postgres;

--
-- TOC entry 261 (class 1259 OID 25246)
-- Name: channel_season_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.channel_season_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.channel_season_id_seq OWNER TO postgres;

--
-- TOC entry 6573 (class 0 OID 0)
-- Dependencies: 261
-- Name: channel_season_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.channel_season_id_seq OWNED BY public.channel_season.id;


--
-- TOC entry 264 (class 1259 OID 25264)
-- Name: channel_social_interact; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.channel_social_interact (
    id integer NOT NULL,
    channel_id integer NOT NULL,
    protocol public.varchar_short NOT NULL,
    uri public.varchar_uri NOT NULL,
    account_id public.varchar_normal,
    account_url public.varchar_url,
    priority integer
);


ALTER TABLE public.channel_social_interact OWNER TO postgres;

--
-- TOC entry 263 (class 1259 OID 25263)
-- Name: channel_social_interact_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.channel_social_interact_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.channel_social_interact_id_seq OWNER TO postgres;

--
-- TOC entry 6576 (class 0 OID 0)
-- Dependencies: 263
-- Name: channel_social_interact_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.channel_social_interact_id_seq OWNED BY public.channel_social_interact.id;


--
-- TOC entry 266 (class 1259 OID 25279)
-- Name: channel_trailer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.channel_trailer (
    id integer NOT NULL,
    channel_id integer NOT NULL,
    url public.varchar_url NOT NULL,
    title public.varchar_normal,
    pub_date timestamp with time zone NOT NULL,
    length integer,
    type public.varchar_short,
    channel_season_id integer
);


ALTER TABLE public.channel_trailer OWNER TO postgres;

--
-- TOC entry 265 (class 1259 OID 25278)
-- Name: channel_trailer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.channel_trailer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.channel_trailer_id_seq OWNER TO postgres;

--
-- TOC entry 6579 (class 0 OID 0)
-- Dependencies: 265
-- Name: channel_trailer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.channel_trailer_id_seq OWNED BY public.channel_trailer.id;


--
-- TOC entry 268 (class 1259 OID 25302)
-- Name: channel_txt; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.channel_txt (
    id integer NOT NULL,
    channel_id integer NOT NULL,
    purpose public.varchar_normal,
    value public.varchar_long NOT NULL
);


ALTER TABLE public.channel_txt OWNER TO postgres;

--
-- TOC entry 267 (class 1259 OID 25301)
-- Name: channel_txt_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.channel_txt_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.channel_txt_id_seq OWNER TO postgres;

--
-- TOC entry 6582 (class 0 OID 0)
-- Dependencies: 267
-- Name: channel_txt_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.channel_txt_id_seq OWNED BY public.channel_txt.id;


--
-- TOC entry 270 (class 1259 OID 25317)
-- Name: channel_value; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.channel_value (
    id integer NOT NULL,
    channel_id integer NOT NULL,
    type public.varchar_short NOT NULL,
    method public.varchar_short NOT NULL,
    suggested double precision
);


ALTER TABLE public.channel_value OWNER TO postgres;

--
-- TOC entry 269 (class 1259 OID 25316)
-- Name: channel_value_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.channel_value_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.channel_value_id_seq OWNER TO postgres;

--
-- TOC entry 6585 (class 0 OID 0)
-- Dependencies: 269
-- Name: channel_value_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.channel_value_id_seq OWNED BY public.channel_value.id;


--
-- TOC entry 272 (class 1259 OID 25332)
-- Name: channel_value_recipient; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.channel_value_recipient (
    id integer NOT NULL,
    channel_value_id integer NOT NULL,
    type public.varchar_short NOT NULL,
    address public.varchar_long NOT NULL,
    split double precision NOT NULL,
    name public.varchar_normal,
    custom_key public.varchar_long,
    custom_value public.varchar_long,
    fee boolean DEFAULT false
);


ALTER TABLE public.channel_value_recipient OWNER TO postgres;

--
-- TOC entry 271 (class 1259 OID 25331)
-- Name: channel_value_recipient_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.channel_value_recipient_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.channel_value_recipient_id_seq OWNER TO postgres;

--
-- TOC entry 6588 (class 0 OID 0)
-- Dependencies: 271
-- Name: channel_value_recipient_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.channel_value_recipient_id_seq OWNED BY public.channel_value_recipient.id;


--
-- TOC entry 358 (class 1259 OID 26059)
-- Name: clip; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clip (
    id integer NOT NULL,
    id_text public.short_id_v2 NOT NULL,
    account_id integer NOT NULL,
    item_id integer NOT NULL,
    start_time public.media_player_time NOT NULL,
    end_time public.media_player_time,
    title public.varchar_normal,
    description public.varchar_long,
    sharable_status_id integer NOT NULL
);


ALTER TABLE public.clip OWNER TO postgres;

--
-- TOC entry 357 (class 1259 OID 26058)
-- Name: clip_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.clip_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.clip_id_seq OWNER TO postgres;

--
-- TOC entry 6591 (class 0 OID 0)
-- Dependencies: 357
-- Name: clip_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.clip_id_seq OWNED BY public.clip.id;


--
-- TOC entry 224 (class 1259 OID 24889)
-- Name: feed; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.feed (
    id integer NOT NULL,
    url public.varchar_url NOT NULL,
    feed_flag_status_id integer NOT NULL,
    is_parsing public.server_time,
    parsing_priority integer DEFAULT 0,
    last_parsed_file_hash public.varchar_md5,
    container_id character varying(12),
    created_at public.server_time_with_default,
    updated_at public.server_time_with_default,
    CONSTRAINT feed_parsing_priority_check CHECK (((parsing_priority >= 0) AND (parsing_priority <= 5)))
);


ALTER TABLE public.feed OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 24876)
-- Name: feed_flag_status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.feed_flag_status (
    id integer NOT NULL,
    status text,
    created_at public.server_time_with_default,
    updated_at public.server_time_with_default,
    CONSTRAINT feed_flag_status_status_check CHECK ((status = ANY (ARRAY['active'::text, 'always-parse'::text, 'spam'::text, 'pending-archive'::text, 'archived'::text, 'takedown'::text])))
);


ALTER TABLE public.feed_flag_status OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 24875)
-- Name: feed_flag_status_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.feed_flag_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.feed_flag_status_id_seq OWNER TO postgres;

--
-- TOC entry 6595 (class 0 OID 0)
-- Dependencies: 221
-- Name: feed_flag_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.feed_flag_status_id_seq OWNED BY public.feed_flag_status.id;


--
-- TOC entry 223 (class 1259 OID 24888)
-- Name: feed_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.feed_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.feed_id_seq OWNER TO postgres;

--
-- TOC entry 6597 (class 0 OID 0)
-- Dependencies: 223
-- Name: feed_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.feed_id_seq OWNED BY public.feed.id;


--
-- TOC entry 226 (class 1259 OID 24909)
-- Name: feed_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.feed_log (
    id integer NOT NULL,
    feed_id integer NOT NULL,
    last_http_status integer,
    last_good_http_status_time public.server_time,
    last_finished_parse_time public.server_time,
    parse_errors integer DEFAULT 0
);


ALTER TABLE public.feed_log OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 24908)
-- Name: feed_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.feed_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.feed_log_id_seq OWNER TO postgres;

--
-- TOC entry 6600 (class 0 OID 0)
-- Dependencies: 225
-- Name: feed_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.feed_log_id_seq OWNED BY public.feed_log.id;


--
-- TOC entry 276 (class 1259 OID 25361)
-- Name: item; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item (
    id integer NOT NULL,
    id_text public.short_id_v2 NOT NULL,
    slug public.varchar_slug,
    channel_id integer NOT NULL,
    guid public.varchar_uri,
    guid_enclosure_url public.varchar_url,
    pub_date timestamp with time zone,
    title public.varchar_normal,
    item_flag_status_id integer NOT NULL,
    CONSTRAINT item_check CHECK (((guid IS NOT NULL) OR (guid_enclosure_url IS NOT NULL)))
);


ALTER TABLE public.item OWNER TO postgres;

--
-- TOC entry 280 (class 1259 OID 25400)
-- Name: item_about; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_about (
    id integer NOT NULL,
    item_id integer NOT NULL,
    duration public.media_player_time,
    explicit boolean,
    website_link_url public.varchar_url,
    item_itunes_episode_type_id integer
);


ALTER TABLE public.item_about OWNER TO postgres;

--
-- TOC entry 279 (class 1259 OID 25399)
-- Name: item_about_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_about_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_about_id_seq OWNER TO postgres;

--
-- TOC entry 6604 (class 0 OID 0)
-- Dependencies: 279
-- Name: item_about_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_about_id_seq OWNED BY public.item_about.id;


--
-- TOC entry 286 (class 1259 OID 25456)
-- Name: item_chapter; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_chapter (
    id integer NOT NULL,
    id_text public.short_id_v2 NOT NULL,
    item_chapters_feed_id integer NOT NULL,
    start_time public.media_player_time NOT NULL,
    end_time public.media_player_time,
    title public.varchar_normal,
    img public.varchar_url,
    web_url public.varchar_url,
    table_of_contents boolean DEFAULT true
);


ALTER TABLE public.item_chapter OWNER TO postgres;

--
-- TOC entry 285 (class 1259 OID 25455)
-- Name: item_chapter_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_chapter_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_chapter_id_seq OWNER TO postgres;

--
-- TOC entry 6607 (class 0 OID 0)
-- Dependencies: 285
-- Name: item_chapter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_chapter_id_seq OWNED BY public.item_chapter.id;


--
-- TOC entry 288 (class 1259 OID 25474)
-- Name: item_chapter_location; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_chapter_location (
    id integer NOT NULL,
    item_chapter_id integer NOT NULL,
    geo public.varchar_normal,
    osm public.varchar_normal,
    name public.varchar_normal,
    CONSTRAINT item_chapter_location_check CHECK (((geo IS NOT NULL) OR (osm IS NOT NULL)))
);


ALTER TABLE public.item_chapter_location OWNER TO postgres;

--
-- TOC entry 287 (class 1259 OID 25473)
-- Name: item_chapter_location_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_chapter_location_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_chapter_location_id_seq OWNER TO postgres;

--
-- TOC entry 6610 (class 0 OID 0)
-- Dependencies: 287
-- Name: item_chapter_location_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_chapter_location_id_seq OWNED BY public.item_chapter_location.id;


--
-- TOC entry 282 (class 1259 OID 25423)
-- Name: item_chapters_feed; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_chapters_feed (
    id integer NOT NULL,
    item_id integer NOT NULL,
    url public.varchar_url NOT NULL,
    type public.varchar_short NOT NULL
);


ALTER TABLE public.item_chapters_feed OWNER TO postgres;

--
-- TOC entry 281 (class 1259 OID 25422)
-- Name: item_chapters_feed_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_chapters_feed_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_chapters_feed_id_seq OWNER TO postgres;

--
-- TOC entry 6613 (class 0 OID 0)
-- Dependencies: 281
-- Name: item_chapters_feed_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_chapters_feed_id_seq OWNED BY public.item_chapters_feed.id;


--
-- TOC entry 284 (class 1259 OID 25440)
-- Name: item_chapters_feed_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_chapters_feed_log (
    id integer NOT NULL,
    item_chapters_feed_id integer NOT NULL,
    last_http_status integer,
    last_good_http_status_time public.server_time,
    last_finished_parse_time public.server_time,
    parse_errors integer DEFAULT 0
);


ALTER TABLE public.item_chapters_feed_log OWNER TO postgres;

--
-- TOC entry 283 (class 1259 OID 25439)
-- Name: item_chapters_feed_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_chapters_feed_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_chapters_feed_log_id_seq OWNER TO postgres;

--
-- TOC entry 6616 (class 0 OID 0)
-- Dependencies: 283
-- Name: item_chapters_feed_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_chapters_feed_log_id_seq OWNED BY public.item_chapters_feed_log.id;


--
-- TOC entry 290 (class 1259 OID 25492)
-- Name: item_chat; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_chat (
    id integer NOT NULL,
    item_id integer NOT NULL,
    server public.varchar_fqdn NOT NULL,
    protocol public.varchar_short NOT NULL,
    account_id public.varchar_normal,
    space public.varchar_normal
);


ALTER TABLE public.item_chat OWNER TO postgres;

--
-- TOC entry 289 (class 1259 OID 25491)
-- Name: item_chat_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_chat_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_chat_id_seq OWNER TO postgres;

--
-- TOC entry 6619 (class 0 OID 0)
-- Dependencies: 289
-- Name: item_chat_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_chat_id_seq OWNED BY public.item_chat.id;


--
-- TOC entry 292 (class 1259 OID 25509)
-- Name: item_content_link; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_content_link (
    id integer NOT NULL,
    item_id integer NOT NULL,
    href public.varchar_url NOT NULL,
    title public.varchar_normal
);


ALTER TABLE public.item_content_link OWNER TO postgres;

--
-- TOC entry 291 (class 1259 OID 25508)
-- Name: item_content_link_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_content_link_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_content_link_id_seq OWNER TO postgres;

--
-- TOC entry 6622 (class 0 OID 0)
-- Dependencies: 291
-- Name: item_content_link_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_content_link_id_seq OWNED BY public.item_content_link.id;


--
-- TOC entry 294 (class 1259 OID 25524)
-- Name: item_description; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_description (
    id integer NOT NULL,
    item_id integer NOT NULL,
    value public.varchar_long NOT NULL
);


ALTER TABLE public.item_description OWNER TO postgres;

--
-- TOC entry 293 (class 1259 OID 25523)
-- Name: item_description_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_description_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_description_id_seq OWNER TO postgres;

--
-- TOC entry 6625 (class 0 OID 0)
-- Dependencies: 293
-- Name: item_description_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_description_id_seq OWNED BY public.item_description.id;


--
-- TOC entry 296 (class 1259 OID 25541)
-- Name: item_enclosure; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_enclosure (
    id integer NOT NULL,
    item_id integer NOT NULL,
    type public.varchar_short NOT NULL,
    length integer,
    bitrate integer,
    height integer,
    language public.varchar_short,
    title public.varchar_short,
    rel public.varchar_short,
    codecs public.varchar_short,
    item_enclosure_default boolean DEFAULT false
);


ALTER TABLE public.item_enclosure OWNER TO postgres;

--
-- TOC entry 295 (class 1259 OID 25540)
-- Name: item_enclosure_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_enclosure_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_enclosure_id_seq OWNER TO postgres;

--
-- TOC entry 6628 (class 0 OID 0)
-- Dependencies: 295
-- Name: item_enclosure_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_enclosure_id_seq OWNED BY public.item_enclosure.id;


--
-- TOC entry 300 (class 1259 OID 25572)
-- Name: item_enclosure_integrity; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_enclosure_integrity (
    id integer NOT NULL,
    item_enclosure_id integer NOT NULL,
    type text NOT NULL,
    value public.varchar_long NOT NULL,
    CONSTRAINT item_enclosure_integrity_type_check CHECK ((type = ANY (ARRAY['sri'::text, 'pgp-signature'::text])))
);


ALTER TABLE public.item_enclosure_integrity OWNER TO postgres;

--
-- TOC entry 299 (class 1259 OID 25571)
-- Name: item_enclosure_integrity_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_enclosure_integrity_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_enclosure_integrity_id_seq OWNER TO postgres;

--
-- TOC entry 6631 (class 0 OID 0)
-- Dependencies: 299
-- Name: item_enclosure_integrity_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_enclosure_integrity_id_seq OWNED BY public.item_enclosure_integrity.id;


--
-- TOC entry 298 (class 1259 OID 25557)
-- Name: item_enclosure_source; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_enclosure_source (
    id integer NOT NULL,
    item_enclosure_id integer NOT NULL,
    uri public.varchar_uri NOT NULL,
    content_type public.varchar_short
);


ALTER TABLE public.item_enclosure_source OWNER TO postgres;

--
-- TOC entry 297 (class 1259 OID 25556)
-- Name: item_enclosure_source_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_enclosure_source_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_enclosure_source_id_seq OWNER TO postgres;

--
-- TOC entry 6634 (class 0 OID 0)
-- Dependencies: 297
-- Name: item_enclosure_source_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_enclosure_source_id_seq OWNED BY public.item_enclosure_source.id;


--
-- TOC entry 274 (class 1259 OID 25348)
-- Name: item_flag_status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_flag_status (
    id integer NOT NULL,
    status text,
    created_at public.server_time_with_default,
    updated_at public.server_time_with_default,
    CONSTRAINT item_flag_status_status_check CHECK ((status = ANY (ARRAY['active'::text, 'pending-archive'::text, 'archived'::text, 'pending-delete'::text])))
);


ALTER TABLE public.item_flag_status OWNER TO postgres;

--
-- TOC entry 273 (class 1259 OID 25347)
-- Name: item_flag_status_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_flag_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_flag_status_id_seq OWNER TO postgres;

--
-- TOC entry 6637 (class 0 OID 0)
-- Dependencies: 273
-- Name: item_flag_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_flag_status_id_seq OWNED BY public.item_flag_status.id;


--
-- TOC entry 302 (class 1259 OID 25590)
-- Name: item_funding; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_funding (
    id integer NOT NULL,
    item_id integer NOT NULL,
    url public.varchar_url NOT NULL,
    title public.varchar_normal
);


ALTER TABLE public.item_funding OWNER TO postgres;

--
-- TOC entry 301 (class 1259 OID 25589)
-- Name: item_funding_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_funding_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_funding_id_seq OWNER TO postgres;

--
-- TOC entry 6640 (class 0 OID 0)
-- Dependencies: 301
-- Name: item_funding_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_funding_id_seq OWNED BY public.item_funding.id;


--
-- TOC entry 275 (class 1259 OID 25360)
-- Name: item_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_id_seq OWNER TO postgres;

--
-- TOC entry 6642 (class 0 OID 0)
-- Dependencies: 275
-- Name: item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_id_seq OWNED BY public.item.id;


--
-- TOC entry 304 (class 1259 OID 25605)
-- Name: item_image; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_image (
    id integer NOT NULL,
    item_id integer NOT NULL,
    url public.varchar_url NOT NULL,
    image_width_size integer,
    is_resized boolean DEFAULT false
);


ALTER TABLE public.item_image OWNER TO postgres;

--
-- TOC entry 303 (class 1259 OID 25604)
-- Name: item_image_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_image_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_image_id_seq OWNER TO postgres;

--
-- TOC entry 6645 (class 0 OID 0)
-- Dependencies: 303
-- Name: item_image_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_image_id_seq OWNED BY public.item_image.id;


--
-- TOC entry 278 (class 1259 OID 25388)
-- Name: item_itunes_episode_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_itunes_episode_type (
    id integer NOT NULL,
    itunes_episode_type text,
    CONSTRAINT item_itunes_episode_type_itunes_episode_type_check CHECK ((itunes_episode_type = ANY (ARRAY['full'::text, 'trailer'::text, 'bonus'::text])))
);


ALTER TABLE public.item_itunes_episode_type OWNER TO postgres;

--
-- TOC entry 277 (class 1259 OID 25387)
-- Name: item_itunes_episode_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_itunes_episode_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_itunes_episode_type_id_seq OWNER TO postgres;

--
-- TOC entry 6648 (class 0 OID 0)
-- Dependencies: 277
-- Name: item_itunes_episode_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_itunes_episode_type_id_seq OWNED BY public.item_itunes_episode_type.id;


--
-- TOC entry 306 (class 1259 OID 25621)
-- Name: item_license; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_license (
    id integer NOT NULL,
    item_id integer NOT NULL,
    identifier public.varchar_normal NOT NULL,
    url public.varchar_url
);


ALTER TABLE public.item_license OWNER TO postgres;

--
-- TOC entry 305 (class 1259 OID 25620)
-- Name: item_license_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_license_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_license_id_seq OWNER TO postgres;

--
-- TOC entry 6651 (class 0 OID 0)
-- Dependencies: 305
-- Name: item_license_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_license_id_seq OWNED BY public.item_license.id;


--
-- TOC entry 308 (class 1259 OID 25638)
-- Name: item_location; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_location (
    id integer NOT NULL,
    item_id integer NOT NULL,
    geo public.varchar_normal,
    osm public.varchar_normal,
    name public.varchar_normal,
    CONSTRAINT item_location_check CHECK (((geo IS NOT NULL) OR (osm IS NOT NULL)))
);


ALTER TABLE public.item_location OWNER TO postgres;

--
-- TOC entry 307 (class 1259 OID 25637)
-- Name: item_location_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_location_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_location_id_seq OWNER TO postgres;

--
-- TOC entry 6654 (class 0 OID 0)
-- Dependencies: 307
-- Name: item_location_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_location_id_seq OWNED BY public.item_location.id;


--
-- TOC entry 310 (class 1259 OID 25656)
-- Name: item_person; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_person (
    id integer NOT NULL,
    item_id integer NOT NULL,
    name public.varchar_normal NOT NULL,
    role public.varchar_normal,
    person_group public.varchar_normal DEFAULT 'cast'::character varying,
    img public.varchar_url,
    href public.varchar_url
);


ALTER TABLE public.item_person OWNER TO postgres;

--
-- TOC entry 309 (class 1259 OID 25655)
-- Name: item_person_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_person_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_person_id_seq OWNER TO postgres;

--
-- TOC entry 6657 (class 0 OID 0)
-- Dependencies: 309
-- Name: item_person_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_person_id_seq OWNED BY public.item_person.id;


--
-- TOC entry 312 (class 1259 OID 25672)
-- Name: item_season; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_season (
    id integer NOT NULL,
    channel_season_id integer NOT NULL,
    item_id integer NOT NULL,
    title public.varchar_normal
);


ALTER TABLE public.item_season OWNER TO postgres;

--
-- TOC entry 314 (class 1259 OID 25693)
-- Name: item_season_episode; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_season_episode (
    id integer NOT NULL,
    item_id integer NOT NULL,
    display public.varchar_short,
    number double precision NOT NULL
);


ALTER TABLE public.item_season_episode OWNER TO postgres;

--
-- TOC entry 313 (class 1259 OID 25692)
-- Name: item_season_episode_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_season_episode_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_season_episode_id_seq OWNER TO postgres;

--
-- TOC entry 6661 (class 0 OID 0)
-- Dependencies: 313
-- Name: item_season_episode_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_season_episode_id_seq OWNED BY public.item_season_episode.id;


--
-- TOC entry 311 (class 1259 OID 25671)
-- Name: item_season_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_season_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_season_id_seq OWNER TO postgres;

--
-- TOC entry 6663 (class 0 OID 0)
-- Dependencies: 311
-- Name: item_season_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_season_id_seq OWNED BY public.item_season.id;


--
-- TOC entry 316 (class 1259 OID 25710)
-- Name: item_social_interact; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_social_interact (
    id integer NOT NULL,
    item_id integer NOT NULL,
    protocol public.varchar_short NOT NULL,
    uri public.varchar_uri NOT NULL,
    account_id public.varchar_normal,
    account_url public.varchar_url,
    priority integer
);


ALTER TABLE public.item_social_interact OWNER TO postgres;

--
-- TOC entry 315 (class 1259 OID 25709)
-- Name: item_social_interact_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_social_interact_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_social_interact_id_seq OWNER TO postgres;

--
-- TOC entry 6666 (class 0 OID 0)
-- Dependencies: 315
-- Name: item_social_interact_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_social_interact_id_seq OWNED BY public.item_social_interact.id;


--
-- TOC entry 318 (class 1259 OID 25725)
-- Name: item_soundbite; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_soundbite (
    id integer NOT NULL,
    id_text public.short_id_v2 NOT NULL,
    item_id integer NOT NULL,
    start_time public.media_player_time NOT NULL,
    duration public.media_player_time NOT NULL,
    title public.varchar_normal
);


ALTER TABLE public.item_soundbite OWNER TO postgres;

--
-- TOC entry 317 (class 1259 OID 25724)
-- Name: item_soundbite_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_soundbite_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_soundbite_id_seq OWNER TO postgres;

--
-- TOC entry 6669 (class 0 OID 0)
-- Dependencies: 317
-- Name: item_soundbite_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_soundbite_id_seq OWNED BY public.item_soundbite.id;


--
-- TOC entry 320 (class 1259 OID 25742)
-- Name: item_transcript; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_transcript (
    id integer NOT NULL,
    item_id integer NOT NULL,
    url public.varchar_url NOT NULL,
    type public.varchar_short NOT NULL,
    language public.varchar_short,
    rel character varying(50),
    CONSTRAINT item_transcript_rel_check CHECK (((rel IS NULL) OR ((rel)::text = 'captions'::text)))
);


ALTER TABLE public.item_transcript OWNER TO postgres;

--
-- TOC entry 319 (class 1259 OID 25741)
-- Name: item_transcript_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_transcript_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_transcript_id_seq OWNER TO postgres;

--
-- TOC entry 6672 (class 0 OID 0)
-- Dependencies: 319
-- Name: item_transcript_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_transcript_id_seq OWNED BY public.item_transcript.id;


--
-- TOC entry 322 (class 1259 OID 25758)
-- Name: item_txt; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_txt (
    id integer NOT NULL,
    item_id integer NOT NULL,
    purpose public.varchar_normal,
    value public.varchar_long NOT NULL
);


ALTER TABLE public.item_txt OWNER TO postgres;

--
-- TOC entry 321 (class 1259 OID 25757)
-- Name: item_txt_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_txt_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_txt_id_seq OWNER TO postgres;

--
-- TOC entry 6675 (class 0 OID 0)
-- Dependencies: 321
-- Name: item_txt_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_txt_id_seq OWNED BY public.item_txt.id;


--
-- TOC entry 324 (class 1259 OID 25773)
-- Name: item_value; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_value (
    id integer NOT NULL,
    item_id integer NOT NULL,
    type public.varchar_short NOT NULL,
    method public.varchar_short NOT NULL,
    suggested double precision
);


ALTER TABLE public.item_value OWNER TO postgres;

--
-- TOC entry 323 (class 1259 OID 25772)
-- Name: item_value_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_value_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_value_id_seq OWNER TO postgres;

--
-- TOC entry 6678 (class 0 OID 0)
-- Dependencies: 323
-- Name: item_value_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_value_id_seq OWNED BY public.item_value.id;


--
-- TOC entry 326 (class 1259 OID 25788)
-- Name: item_value_recipient; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_value_recipient (
    id integer NOT NULL,
    item_value_id integer NOT NULL,
    type public.varchar_short NOT NULL,
    address public.varchar_long NOT NULL,
    split double precision NOT NULL,
    name public.varchar_normal,
    custom_key public.varchar_long,
    custom_value public.varchar_long,
    fee boolean DEFAULT false
);


ALTER TABLE public.item_value_recipient OWNER TO postgres;

--
-- TOC entry 325 (class 1259 OID 25787)
-- Name: item_value_recipient_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_value_recipient_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_value_recipient_id_seq OWNER TO postgres;

--
-- TOC entry 6681 (class 0 OID 0)
-- Dependencies: 325
-- Name: item_value_recipient_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_value_recipient_id_seq OWNED BY public.item_value_recipient.id;


--
-- TOC entry 328 (class 1259 OID 25804)
-- Name: item_value_time_split; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_value_time_split (
    id integer NOT NULL,
    item_value_id integer NOT NULL,
    start_time public.media_player_time NOT NULL,
    duration public.media_player_time NOT NULL,
    remote_start_time public.media_player_time DEFAULT 0,
    remote_percentage public.media_player_time DEFAULT 100
);


ALTER TABLE public.item_value_time_split OWNER TO postgres;

--
-- TOC entry 327 (class 1259 OID 25803)
-- Name: item_value_time_split_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_value_time_split_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_value_time_split_id_seq OWNER TO postgres;

--
-- TOC entry 6684 (class 0 OID 0)
-- Dependencies: 327
-- Name: item_value_time_split_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_value_time_split_id_seq OWNED BY public.item_value_time_split.id;


--
-- TOC entry 332 (class 1259 OID 25841)
-- Name: item_value_time_split_recipient; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_value_time_split_recipient (
    id integer NOT NULL,
    item_value_time_split_id integer NOT NULL,
    type public.varchar_short NOT NULL,
    address public.varchar_long NOT NULL,
    split double precision NOT NULL,
    name public.varchar_normal,
    custom_key public.varchar_long,
    custom_value public.varchar_long,
    fee boolean DEFAULT false
);


ALTER TABLE public.item_value_time_split_recipient OWNER TO postgres;

--
-- TOC entry 331 (class 1259 OID 25840)
-- Name: item_value_time_split_recipient_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_value_time_split_recipient_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_value_time_split_recipient_id_seq OWNER TO postgres;

--
-- TOC entry 6687 (class 0 OID 0)
-- Dependencies: 331
-- Name: item_value_time_split_recipient_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_value_time_split_recipient_id_seq OWNED BY public.item_value_time_split_recipient.id;


--
-- TOC entry 330 (class 1259 OID 25821)
-- Name: item_value_time_split_remote_item; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_value_time_split_remote_item (
    id integer NOT NULL,
    item_value_time_split_id integer NOT NULL,
    feed_guid uuid NOT NULL,
    feed_url public.varchar_url,
    item_guid public.varchar_uri,
    title public.varchar_normal
);


ALTER TABLE public.item_value_time_split_remote_item OWNER TO postgres;

--
-- TOC entry 329 (class 1259 OID 25820)
-- Name: item_value_time_split_remote_item_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.item_value_time_split_remote_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.item_value_time_split_remote_item_id_seq OWNER TO postgres;

--
-- TOC entry 6690 (class 0 OID 0)
-- Dependencies: 329
-- Name: item_value_time_split_remote_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.item_value_time_split_remote_item_id_seq OWNED BY public.item_value_time_split_remote_item.id;


--
-- TOC entry 336 (class 1259 OID 25869)
-- Name: live_item; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.live_item (
    id integer NOT NULL,
    item_id integer NOT NULL,
    live_item_status_id integer NOT NULL,
    start_time timestamp with time zone NOT NULL,
    end_time timestamp with time zone,
    chat_web_url public.varchar_url
);


ALTER TABLE public.live_item OWNER TO postgres;

--
-- TOC entry 335 (class 1259 OID 25868)
-- Name: live_item_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.live_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.live_item_id_seq OWNER TO postgres;

--
-- TOC entry 6693 (class 0 OID 0)
-- Dependencies: 335
-- Name: live_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.live_item_id_seq OWNED BY public.live_item.id;


--
-- TOC entry 334 (class 1259 OID 25857)
-- Name: live_item_status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.live_item_status (
    id integer NOT NULL,
    status text,
    CONSTRAINT live_item_status_status_check CHECK ((status = ANY (ARRAY['pending'::text, 'live'::text, 'ended'::text])))
);


ALTER TABLE public.live_item_status OWNER TO postgres;

--
-- TOC entry 333 (class 1259 OID 25856)
-- Name: live_item_status_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.live_item_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.live_item_status_id_seq OWNER TO postgres;

--
-- TOC entry 6696 (class 0 OID 0)
-- Dependencies: 333
-- Name: live_item_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.live_item_status_id_seq OWNED BY public.live_item_status.id;


--
-- TOC entry 220 (class 1259 OID 24864)
-- Name: medium; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.medium (
    id integer NOT NULL,
    value text,
    CONSTRAINT medium_value_check CHECK ((value = ANY (ARRAY['publisher'::text, 'podcast'::text, 'music'::text, 'video'::text, 'film'::text, 'audiobook'::text, 'newsletter'::text, 'blog'::text, 'publisher'::text, 'course'::text, 'mixed'::text, 'podcastL'::text, 'musicL'::text, 'videoL'::text, 'filmL'::text, 'audiobookL'::text, 'newsletterL'::text, 'blogL'::text, 'publisherL'::text, 'courseL'::text])))
);


ALTER TABLE public.medium OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 24863)
-- Name: medium_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.medium_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.medium_id_seq OWNER TO postgres;

--
-- TOC entry 6699 (class 0 OID 0)
-- Dependencies: 219
-- Name: medium_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.medium_id_seq OWNED BY public.medium.id;


--
-- TOC entry 379 (class 1259 OID 26413)
-- Name: membership_claim_token; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.membership_claim_token (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    claimed boolean DEFAULT false,
    months_to_add integer DEFAULT 1,
    account_membership_id integer
);


ALTER TABLE public.membership_claim_token OWNER TO postgres;

--
-- TOC entry 360 (class 1259 OID 26088)
-- Name: playlist; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.playlist (
    id integer NOT NULL,
    id_text public.short_id_v2 NOT NULL,
    account_id integer NOT NULL,
    sharable_status_id integer NOT NULL,
    title public.varchar_normal,
    description public.varchar_long,
    is_default_favorites boolean DEFAULT false,
    item_count integer DEFAULT 0,
    medium_id integer NOT NULL
);


ALTER TABLE public.playlist OWNER TO postgres;

--
-- TOC entry 359 (class 1259 OID 26087)
-- Name: playlist_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.playlist_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.playlist_id_seq OWNER TO postgres;

--
-- TOC entry 6703 (class 0 OID 0)
-- Dependencies: 359
-- Name: playlist_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.playlist_id_seq OWNED BY public.playlist.id;


--
-- TOC entry 362 (class 1259 OID 26120)
-- Name: playlist_resource; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.playlist_resource (
    id integer NOT NULL,
    playlist_id integer NOT NULL,
    list_position public.list_position NOT NULL,
    item_id integer,
    item_chapter_id integer,
    clip_id integer,
    item_soundbite_id integer,
    add_by_rss_resource_data jsonb,
    add_by_rss_hash_id public.varchar_md5,
    CONSTRAINT playlist_resource_check CHECK ((((((((item_id IS NOT NULL))::integer + ((add_by_rss_hash_id IS NOT NULL))::integer) + ((item_chapter_id IS NOT NULL))::integer) + ((clip_id IS NOT NULL))::integer) + ((item_soundbite_id IS NOT NULL))::integer) = 1))
);


ALTER TABLE public.playlist_resource OWNER TO postgres;

--
-- TOC entry 361 (class 1259 OID 26119)
-- Name: playlist_resource_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.playlist_resource_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.playlist_resource_id_seq OWNER TO postgres;

--
-- TOC entry 6706 (class 0 OID 0)
-- Dependencies: 361
-- Name: playlist_resource_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.playlist_resource_id_seq OWNED BY public.playlist_resource.id;


--
-- TOC entry 364 (class 1259 OID 26175)
-- Name: queue; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.queue (
    id integer NOT NULL,
    id_text public.short_id_v2 NOT NULL,
    account_id integer NOT NULL,
    medium_id integer NOT NULL
);


ALTER TABLE public.queue OWNER TO postgres;

--
-- TOC entry 363 (class 1259 OID 26174)
-- Name: queue_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.queue_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.queue_id_seq OWNER TO postgres;

--
-- TOC entry 6709 (class 0 OID 0)
-- Dependencies: 363
-- Name: queue_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.queue_id_seq OWNED BY public.queue.id;


--
-- TOC entry 366 (class 1259 OID 26200)
-- Name: queue_resource; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.queue_resource (
    id integer NOT NULL,
    queue_id integer NOT NULL,
    list_position public.list_position NOT NULL,
    playback_position public.media_player_time DEFAULT 0 NOT NULL,
    media_file_duration public.media_player_time DEFAULT 0 NOT NULL,
    completed boolean DEFAULT false NOT NULL,
    item_id integer,
    item_chapter_id integer,
    clip_id integer,
    item_soundbite_id integer,
    add_by_rss_resource_data jsonb,
    add_by_rss_hash_id public.varchar_md5,
    CONSTRAINT queue_resource_check CHECK ((((((((item_id IS NOT NULL))::integer + ((add_by_rss_hash_id IS NOT NULL))::integer) + ((item_chapter_id IS NOT NULL))::integer) + ((clip_id IS NOT NULL))::integer) + ((item_soundbite_id IS NOT NULL))::integer) = 1))
);


ALTER TABLE public.queue_resource OWNER TO postgres;

--
-- TOC entry 365 (class 1259 OID 26199)
-- Name: queue_resource_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.queue_resource_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.queue_resource_id_seq OWNER TO postgres;

--
-- TOC entry 6712 (class 0 OID 0)
-- Dependencies: 365
-- Name: queue_resource_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.queue_resource_id_seq OWNED BY public.queue_resource.id;


--
-- TOC entry 338 (class 1259 OID 25892)
-- Name: sharable_status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sharable_status (
    id integer NOT NULL,
    status text,
    CONSTRAINT sharable_status_status_check CHECK ((status = ANY (ARRAY['public'::text, 'unlisted'::text, 'private'::text])))
);


ALTER TABLE public.sharable_status OWNER TO postgres;

--
-- TOC entry 337 (class 1259 OID 25891)
-- Name: sharable_status_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sharable_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sharable_status_id_seq OWNER TO postgres;

--
-- TOC entry 6715 (class 0 OID 0)
-- Dependencies: 337
-- Name: sharable_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sharable_status_id_seq OWNED BY public.sharable_status.id;


--
-- TOC entry 401 (class 1259 OID 26701)
-- Name: stats_aggregated_account; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stats_aggregated_account (
    id integer NOT NULL,
    tracked_account_id integer NOT NULL,
    day_current_count integer DEFAULT 0 NOT NULL,
    day_1_count integer DEFAULT 0 NOT NULL,
    day_2_count integer DEFAULT 0 NOT NULL,
    day_3_count integer DEFAULT 0 NOT NULL,
    day_4_count integer DEFAULT 0 NOT NULL,
    day_5_count integer DEFAULT 0 NOT NULL,
    day_6_count integer DEFAULT 0 NOT NULL,
    day_7_count integer DEFAULT 0 NOT NULL,
    day_8_count integer DEFAULT 0 NOT NULL,
    week_current_count integer DEFAULT 0 NOT NULL,
    week_1_count integer DEFAULT 0 NOT NULL,
    week_2_count integer DEFAULT 0 NOT NULL,
    week_3_count integer DEFAULT 0 NOT NULL,
    week_4_count integer DEFAULT 0 NOT NULL,
    month_current_count integer DEFAULT 0 NOT NULL,
    month_1_count integer DEFAULT 0 NOT NULL,
    all_time_count integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.stats_aggregated_account OWNER TO postgres;

--
-- TOC entry 400 (class 1259 OID 26700)
-- Name: stats_aggregated_account_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.stats_aggregated_account_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.stats_aggregated_account_id_seq OWNER TO postgres;

--
-- TOC entry 6718 (class 0 OID 0)
-- Dependencies: 400
-- Name: stats_aggregated_account_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.stats_aggregated_account_id_seq OWNED BY public.stats_aggregated_account.id;


--
-- TOC entry 385 (class 1259 OID 26469)
-- Name: stats_aggregated_channel; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stats_aggregated_channel (
    id integer NOT NULL,
    channel_id integer NOT NULL,
    day_current_count integer DEFAULT 0 NOT NULL,
    day_1_count integer DEFAULT 0 NOT NULL,
    day_2_count integer DEFAULT 0 NOT NULL,
    day_3_count integer DEFAULT 0 NOT NULL,
    day_4_count integer DEFAULT 0 NOT NULL,
    day_5_count integer DEFAULT 0 NOT NULL,
    day_6_count integer DEFAULT 0 NOT NULL,
    day_7_count integer DEFAULT 0 NOT NULL,
    day_8_count integer DEFAULT 0 NOT NULL,
    week_current_count integer DEFAULT 0 NOT NULL,
    week_1_count integer DEFAULT 0 NOT NULL,
    week_2_count integer DEFAULT 0 NOT NULL,
    week_3_count integer DEFAULT 0 NOT NULL,
    week_4_count integer DEFAULT 0 NOT NULL,
    month_current_count integer DEFAULT 0 NOT NULL,
    month_1_count integer DEFAULT 0 NOT NULL,
    all_time_count integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.stats_aggregated_channel OWNER TO postgres;

--
-- TOC entry 384 (class 1259 OID 26468)
-- Name: stats_aggregated_channel_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.stats_aggregated_channel_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.stats_aggregated_channel_id_seq OWNER TO postgres;

--
-- TOC entry 6721 (class 0 OID 0)
-- Dependencies: 384
-- Name: stats_aggregated_channel_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.stats_aggregated_channel_id_seq OWNED BY public.stats_aggregated_channel.id;


--
-- TOC entry 393 (class 1259 OID 26585)
-- Name: stats_aggregated_clip; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stats_aggregated_clip (
    id integer NOT NULL,
    clip_id integer NOT NULL,
    day_current_count integer DEFAULT 0 NOT NULL,
    day_1_count integer DEFAULT 0 NOT NULL,
    day_2_count integer DEFAULT 0 NOT NULL,
    day_3_count integer DEFAULT 0 NOT NULL,
    day_4_count integer DEFAULT 0 NOT NULL,
    day_5_count integer DEFAULT 0 NOT NULL,
    day_6_count integer DEFAULT 0 NOT NULL,
    day_7_count integer DEFAULT 0 NOT NULL,
    day_8_count integer DEFAULT 0 NOT NULL,
    week_current_count integer DEFAULT 0 NOT NULL,
    week_1_count integer DEFAULT 0 NOT NULL,
    week_2_count integer DEFAULT 0 NOT NULL,
    week_3_count integer DEFAULT 0 NOT NULL,
    week_4_count integer DEFAULT 0 NOT NULL,
    month_current_count integer DEFAULT 0 NOT NULL,
    month_1_count integer DEFAULT 0 NOT NULL,
    all_time_count integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.stats_aggregated_clip OWNER TO postgres;

--
-- TOC entry 392 (class 1259 OID 26584)
-- Name: stats_aggregated_clip_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.stats_aggregated_clip_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.stats_aggregated_clip_id_seq OWNER TO postgres;

--
-- TOC entry 6724 (class 0 OID 0)
-- Dependencies: 392
-- Name: stats_aggregated_clip_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.stats_aggregated_clip_id_seq OWNED BY public.stats_aggregated_clip.id;


--
-- TOC entry 389 (class 1259 OID 26527)
-- Name: stats_aggregated_item; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stats_aggregated_item (
    id integer NOT NULL,
    item_id integer NOT NULL,
    day_current_count integer DEFAULT 0 NOT NULL,
    day_1_count integer DEFAULT 0 NOT NULL,
    day_2_count integer DEFAULT 0 NOT NULL,
    day_3_count integer DEFAULT 0 NOT NULL,
    day_4_count integer DEFAULT 0 NOT NULL,
    day_5_count integer DEFAULT 0 NOT NULL,
    day_6_count integer DEFAULT 0 NOT NULL,
    day_7_count integer DEFAULT 0 NOT NULL,
    day_8_count integer DEFAULT 0 NOT NULL,
    week_current_count integer DEFAULT 0 NOT NULL,
    week_1_count integer DEFAULT 0 NOT NULL,
    week_2_count integer DEFAULT 0 NOT NULL,
    week_3_count integer DEFAULT 0 NOT NULL,
    week_4_count integer DEFAULT 0 NOT NULL,
    month_current_count integer DEFAULT 0 NOT NULL,
    month_1_count integer DEFAULT 0 NOT NULL,
    all_time_count integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.stats_aggregated_item OWNER TO postgres;

--
-- TOC entry 388 (class 1259 OID 26526)
-- Name: stats_aggregated_item_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.stats_aggregated_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.stats_aggregated_item_id_seq OWNER TO postgres;

--
-- TOC entry 6727 (class 0 OID 0)
-- Dependencies: 388
-- Name: stats_aggregated_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.stats_aggregated_item_id_seq OWNED BY public.stats_aggregated_item.id;


--
-- TOC entry 397 (class 1259 OID 26643)
-- Name: stats_aggregated_playlist; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stats_aggregated_playlist (
    id integer NOT NULL,
    playlist_id integer NOT NULL,
    day_current_count integer DEFAULT 0 NOT NULL,
    day_1_count integer DEFAULT 0 NOT NULL,
    day_2_count integer DEFAULT 0 NOT NULL,
    day_3_count integer DEFAULT 0 NOT NULL,
    day_4_count integer DEFAULT 0 NOT NULL,
    day_5_count integer DEFAULT 0 NOT NULL,
    day_6_count integer DEFAULT 0 NOT NULL,
    day_7_count integer DEFAULT 0 NOT NULL,
    day_8_count integer DEFAULT 0 NOT NULL,
    week_current_count integer DEFAULT 0 NOT NULL,
    week_1_count integer DEFAULT 0 NOT NULL,
    week_2_count integer DEFAULT 0 NOT NULL,
    week_3_count integer DEFAULT 0 NOT NULL,
    week_4_count integer DEFAULT 0 NOT NULL,
    month_current_count integer DEFAULT 0 NOT NULL,
    month_1_count integer DEFAULT 0 NOT NULL,
    all_time_count integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.stats_aggregated_playlist OWNER TO postgres;

--
-- TOC entry 396 (class 1259 OID 26642)
-- Name: stats_aggregated_playlist_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.stats_aggregated_playlist_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.stats_aggregated_playlist_id_seq OWNER TO postgres;

--
-- TOC entry 6730 (class 0 OID 0)
-- Dependencies: 396
-- Name: stats_aggregated_playlist_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.stats_aggregated_playlist_id_seq OWNED BY public.stats_aggregated_playlist.id;


--
-- TOC entry 381 (class 1259 OID 26428)
-- Name: stats_track_account_guid; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stats_track_account_guid (
    id integer NOT NULL,
    account_id integer NOT NULL,
    account_guid uuid NOT NULL,
    updated_at public.server_time_with_default NOT NULL
);


ALTER TABLE public.stats_track_account_guid OWNER TO postgres;

--
-- TOC entry 380 (class 1259 OID 26427)
-- Name: stats_track_account_guid_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.stats_track_account_guid_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.stats_track_account_guid_id_seq OWNER TO postgres;

--
-- TOC entry 6733 (class 0 OID 0)
-- Dependencies: 380
-- Name: stats_track_account_guid_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.stats_track_account_guid_id_seq OWNED BY public.stats_track_account_guid.id;


--
-- TOC entry 399 (class 1259 OID 26679)
-- Name: stats_track_event_account; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stats_track_event_account (
    id integer NOT NULL,
    account_guid uuid NOT NULL,
    tracked_account_id integer NOT NULL,
    created_at public.server_time_with_default NOT NULL
);


ALTER TABLE public.stats_track_event_account OWNER TO postgres;

--
-- TOC entry 398 (class 1259 OID 26678)
-- Name: stats_track_event_account_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.stats_track_event_account_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.stats_track_event_account_id_seq OWNER TO postgres;

--
-- TOC entry 6736 (class 0 OID 0)
-- Dependencies: 398
-- Name: stats_track_event_account_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.stats_track_event_account_id_seq OWNED BY public.stats_track_event_account.id;


--
-- TOC entry 383 (class 1259 OID 26447)
-- Name: stats_track_event_channel; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stats_track_event_channel (
    id integer NOT NULL,
    account_guid uuid NOT NULL,
    channel_id integer NOT NULL,
    created_at public.server_time_with_default NOT NULL
);


ALTER TABLE public.stats_track_event_channel OWNER TO postgres;

--
-- TOC entry 382 (class 1259 OID 26446)
-- Name: stats_track_event_channel_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.stats_track_event_channel_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.stats_track_event_channel_id_seq OWNER TO postgres;

--
-- TOC entry 6739 (class 0 OID 0)
-- Dependencies: 382
-- Name: stats_track_event_channel_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.stats_track_event_channel_id_seq OWNED BY public.stats_track_event_channel.id;


--
-- TOC entry 391 (class 1259 OID 26563)
-- Name: stats_track_event_clip; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stats_track_event_clip (
    id integer NOT NULL,
    account_guid uuid NOT NULL,
    clip_id integer NOT NULL,
    created_at public.server_time_with_default NOT NULL
);


ALTER TABLE public.stats_track_event_clip OWNER TO postgres;

--
-- TOC entry 390 (class 1259 OID 26562)
-- Name: stats_track_event_clip_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.stats_track_event_clip_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.stats_track_event_clip_id_seq OWNER TO postgres;

--
-- TOC entry 6742 (class 0 OID 0)
-- Dependencies: 390
-- Name: stats_track_event_clip_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.stats_track_event_clip_id_seq OWNED BY public.stats_track_event_clip.id;


--
-- TOC entry 387 (class 1259 OID 26505)
-- Name: stats_track_event_item; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stats_track_event_item (
    id integer NOT NULL,
    account_guid uuid NOT NULL,
    item_id integer NOT NULL,
    created_at public.server_time_with_default NOT NULL
);


ALTER TABLE public.stats_track_event_item OWNER TO postgres;

--
-- TOC entry 386 (class 1259 OID 26504)
-- Name: stats_track_event_item_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.stats_track_event_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.stats_track_event_item_id_seq OWNER TO postgres;

--
-- TOC entry 6745 (class 0 OID 0)
-- Dependencies: 386
-- Name: stats_track_event_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.stats_track_event_item_id_seq OWNED BY public.stats_track_event_item.id;


--
-- TOC entry 395 (class 1259 OID 26621)
-- Name: stats_track_event_playlist; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stats_track_event_playlist (
    id integer NOT NULL,
    account_guid uuid NOT NULL,
    playlist_id integer NOT NULL,
    created_at public.server_time_with_default NOT NULL
);


ALTER TABLE public.stats_track_event_playlist OWNER TO postgres;

--
-- TOC entry 394 (class 1259 OID 26620)
-- Name: stats_track_event_playlist_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.stats_track_event_playlist_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.stats_track_event_playlist_id_seq OWNER TO postgres;

--
-- TOC entry 6748 (class 0 OID 0)
-- Dependencies: 394
-- Name: stats_track_event_playlist_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.stats_track_event_playlist_id_seq OWNED BY public.stats_track_event_playlist.id;


--
-- TOC entry 5350 (class 2604 OID 25907)
-- Name: account id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account ALTER COLUMN id SET DEFAULT nextval('public.account_id_seq'::regclass);


--
-- TOC entry 5359 (class 2604 OID 26045)
-- Name: account_admin_roles id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_admin_roles ALTER COLUMN id SET DEFAULT nextval('public.account_admin_roles_id_seq'::regclass);


--
-- TOC entry 5352 (class 2604 OID 25925)
-- Name: account_credentials id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_credentials ALTER COLUMN id SET DEFAULT nextval('public.account_credentials_id_seq'::regclass);


--
-- TOC entry 5356 (class 2604 OID 25995)
-- Name: account_email_change_verification id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_email_change_verification ALTER COLUMN id SET DEFAULT nextval('public.account_email_change_verification_id_seq'::regclass);


--
-- TOC entry 5373 (class 2604 OID 26358)
-- Name: account_fcm_device id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_fcm_device ALTER COLUMN id SET DEFAULT nextval('public.account_fcm_device_id_seq'::regclass);


--
-- TOC entry 5357 (class 2604 OID 26012)
-- Name: account_membership id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_membership ALTER COLUMN id SET DEFAULT nextval('public.account_membership_id_seq'::regclass);


--
-- TOC entry 5358 (class 2604 OID 26024)
-- Name: account_membership_status id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_membership_status ALTER COLUMN id SET DEFAULT nextval('public.account_membership_status_id_seq'::regclass);


--
-- TOC entry 5353 (class 2604 OID 25944)
-- Name: account_profile id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_profile ALTER COLUMN id SET DEFAULT nextval('public.account_profile_id_seq'::regclass);


--
-- TOC entry 5354 (class 2604 OID 25961)
-- Name: account_reset_password id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_reset_password ALTER COLUMN id SET DEFAULT nextval('public.account_reset_password_id_seq'::regclass);


--
-- TOC entry 5372 (class 2604 OID 26340)
-- Name: account_up_device id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_up_device ALTER COLUMN id SET DEFAULT nextval('public.account_up_device_id_seq'::regclass);


--
-- TOC entry 5355 (class 2604 OID 25978)
-- Name: account_verification id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_verification ALTER COLUMN id SET DEFAULT nextval('public.account_verification_id_seq'::regclass);


--
-- TOC entry 5273 (class 2604 OID 24852)
-- Name: category id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.category ALTER COLUMN id SET DEFAULT nextval('public.category_id_seq'::regclass);


--
-- TOC entry 5280 (class 2604 OID 24928)
-- Name: channel id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel ALTER COLUMN id SET DEFAULT nextval('public.channel_id_seq'::regclass);


--
-- TOC entry 5284 (class 2604 OID 24973)
-- Name: channel_about id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_about ALTER COLUMN id SET DEFAULT nextval('public.channel_about_id_seq'::regclass);


--
-- TOC entry 5285 (class 2604 OID 24996)
-- Name: channel_category id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_category ALTER COLUMN id SET DEFAULT nextval('public.channel_category_id_seq'::regclass);


--
-- TOC entry 5286 (class 2604 OID 25015)
-- Name: channel_chat id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_chat ALTER COLUMN id SET DEFAULT nextval('public.channel_chat_id_seq'::regclass);


--
-- TOC entry 5287 (class 2604 OID 25032)
-- Name: channel_description id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_description ALTER COLUMN id SET DEFAULT nextval('public.channel_description_id_seq'::regclass);


--
-- TOC entry 5288 (class 2604 OID 25049)
-- Name: channel_funding id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_funding ALTER COLUMN id SET DEFAULT nextval('public.channel_funding_id_seq'::regclass);


--
-- TOC entry 5289 (class 2604 OID 25064)
-- Name: channel_image id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_image ALTER COLUMN id SET DEFAULT nextval('public.channel_image_id_seq'::regclass);


--
-- TOC entry 5291 (class 2604 OID 25080)
-- Name: channel_internal_settings id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_internal_settings ALTER COLUMN id SET DEFAULT nextval('public.channel_internal_settings_id_seq'::regclass);


--
-- TOC entry 5283 (class 2604 OID 24961)
-- Name: channel_itunes_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_itunes_type ALTER COLUMN id SET DEFAULT nextval('public.channel_itunes_type_id_seq'::regclass);


--
-- TOC entry 5292 (class 2604 OID 25095)
-- Name: channel_license id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_license ALTER COLUMN id SET DEFAULT nextval('public.channel_license_id_seq'::regclass);


--
-- TOC entry 5293 (class 2604 OID 25112)
-- Name: channel_location id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_location ALTER COLUMN id SET DEFAULT nextval('public.channel_location_id_seq'::regclass);


--
-- TOC entry 5294 (class 2604 OID 25130)
-- Name: channel_person id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_person ALTER COLUMN id SET DEFAULT nextval('public.channel_person_id_seq'::regclass);


--
-- TOC entry 5296 (class 2604 OID 25146)
-- Name: channel_podroll id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_podroll ALTER COLUMN id SET DEFAULT nextval('public.channel_podroll_id_seq'::regclass);


--
-- TOC entry 5297 (class 2604 OID 25161)
-- Name: channel_podroll_remote_item id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_podroll_remote_item ALTER COLUMN id SET DEFAULT nextval('public.channel_podroll_remote_item_id_seq'::regclass);


--
-- TOC entry 5298 (class 2604 OID 25185)
-- Name: channel_publisher id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_publisher ALTER COLUMN id SET DEFAULT nextval('public.channel_publisher_id_seq'::regclass);


--
-- TOC entry 5299 (class 2604 OID 25200)
-- Name: channel_publisher_remote_item id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_publisher_remote_item ALTER COLUMN id SET DEFAULT nextval('public.channel_publisher_remote_item_id_seq'::regclass);


--
-- TOC entry 5300 (class 2604 OID 25226)
-- Name: channel_remote_item id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_remote_item ALTER COLUMN id SET DEFAULT nextval('public.channel_remote_item_id_seq'::regclass);


--
-- TOC entry 5301 (class 2604 OID 25250)
-- Name: channel_season id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_season ALTER COLUMN id SET DEFAULT nextval('public.channel_season_id_seq'::regclass);


--
-- TOC entry 5302 (class 2604 OID 25267)
-- Name: channel_social_interact id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_social_interact ALTER COLUMN id SET DEFAULT nextval('public.channel_social_interact_id_seq'::regclass);


--
-- TOC entry 5303 (class 2604 OID 25282)
-- Name: channel_trailer id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_trailer ALTER COLUMN id SET DEFAULT nextval('public.channel_trailer_id_seq'::regclass);


--
-- TOC entry 5304 (class 2604 OID 25305)
-- Name: channel_txt id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_txt ALTER COLUMN id SET DEFAULT nextval('public.channel_txt_id_seq'::regclass);


--
-- TOC entry 5305 (class 2604 OID 25320)
-- Name: channel_value id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_value ALTER COLUMN id SET DEFAULT nextval('public.channel_value_id_seq'::regclass);


--
-- TOC entry 5306 (class 2604 OID 25335)
-- Name: channel_value_recipient id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_value_recipient ALTER COLUMN id SET DEFAULT nextval('public.channel_value_recipient_id_seq'::regclass);


--
-- TOC entry 5362 (class 2604 OID 26062)
-- Name: clip id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clip ALTER COLUMN id SET DEFAULT nextval('public.clip_id_seq'::regclass);


--
-- TOC entry 5276 (class 2604 OID 24892)
-- Name: feed id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.feed ALTER COLUMN id SET DEFAULT nextval('public.feed_id_seq'::regclass);


--
-- TOC entry 5275 (class 2604 OID 24879)
-- Name: feed_flag_status id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.feed_flag_status ALTER COLUMN id SET DEFAULT nextval('public.feed_flag_status_id_seq'::regclass);


--
-- TOC entry 5278 (class 2604 OID 24912)
-- Name: feed_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.feed_log ALTER COLUMN id SET DEFAULT nextval('public.feed_log_id_seq'::regclass);


--
-- TOC entry 5309 (class 2604 OID 25364)
-- Name: item id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item ALTER COLUMN id SET DEFAULT nextval('public.item_id_seq'::regclass);


--
-- TOC entry 5311 (class 2604 OID 25403)
-- Name: item_about id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_about ALTER COLUMN id SET DEFAULT nextval('public.item_about_id_seq'::regclass);


--
-- TOC entry 5315 (class 2604 OID 25459)
-- Name: item_chapter id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_chapter ALTER COLUMN id SET DEFAULT nextval('public.item_chapter_id_seq'::regclass);


--
-- TOC entry 5317 (class 2604 OID 25477)
-- Name: item_chapter_location id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_chapter_location ALTER COLUMN id SET DEFAULT nextval('public.item_chapter_location_id_seq'::regclass);


--
-- TOC entry 5312 (class 2604 OID 25426)
-- Name: item_chapters_feed id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_chapters_feed ALTER COLUMN id SET DEFAULT nextval('public.item_chapters_feed_id_seq'::regclass);


--
-- TOC entry 5313 (class 2604 OID 25443)
-- Name: item_chapters_feed_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_chapters_feed_log ALTER COLUMN id SET DEFAULT nextval('public.item_chapters_feed_log_id_seq'::regclass);


--
-- TOC entry 5318 (class 2604 OID 25495)
-- Name: item_chat id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_chat ALTER COLUMN id SET DEFAULT nextval('public.item_chat_id_seq'::regclass);


--
-- TOC entry 5319 (class 2604 OID 25512)
-- Name: item_content_link id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_content_link ALTER COLUMN id SET DEFAULT nextval('public.item_content_link_id_seq'::regclass);


--
-- TOC entry 5320 (class 2604 OID 25527)
-- Name: item_description id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_description ALTER COLUMN id SET DEFAULT nextval('public.item_description_id_seq'::regclass);


--
-- TOC entry 5321 (class 2604 OID 25544)
-- Name: item_enclosure id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_enclosure ALTER COLUMN id SET DEFAULT nextval('public.item_enclosure_id_seq'::regclass);


--
-- TOC entry 5324 (class 2604 OID 25575)
-- Name: item_enclosure_integrity id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_enclosure_integrity ALTER COLUMN id SET DEFAULT nextval('public.item_enclosure_integrity_id_seq'::regclass);


--
-- TOC entry 5323 (class 2604 OID 25560)
-- Name: item_enclosure_source id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_enclosure_source ALTER COLUMN id SET DEFAULT nextval('public.item_enclosure_source_id_seq'::regclass);


--
-- TOC entry 5308 (class 2604 OID 25351)
-- Name: item_flag_status id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_flag_status ALTER COLUMN id SET DEFAULT nextval('public.item_flag_status_id_seq'::regclass);


--
-- TOC entry 5325 (class 2604 OID 25593)
-- Name: item_funding id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_funding ALTER COLUMN id SET DEFAULT nextval('public.item_funding_id_seq'::regclass);


--
-- TOC entry 5326 (class 2604 OID 25608)
-- Name: item_image id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_image ALTER COLUMN id SET DEFAULT nextval('public.item_image_id_seq'::regclass);


--
-- TOC entry 5310 (class 2604 OID 25391)
-- Name: item_itunes_episode_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_itunes_episode_type ALTER COLUMN id SET DEFAULT nextval('public.item_itunes_episode_type_id_seq'::regclass);


--
-- TOC entry 5328 (class 2604 OID 25624)
-- Name: item_license id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_license ALTER COLUMN id SET DEFAULT nextval('public.item_license_id_seq'::regclass);


--
-- TOC entry 5329 (class 2604 OID 25641)
-- Name: item_location id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_location ALTER COLUMN id SET DEFAULT nextval('public.item_location_id_seq'::regclass);


--
-- TOC entry 5330 (class 2604 OID 25659)
-- Name: item_person id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_person ALTER COLUMN id SET DEFAULT nextval('public.item_person_id_seq'::regclass);


--
-- TOC entry 5332 (class 2604 OID 25675)
-- Name: item_season id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_season ALTER COLUMN id SET DEFAULT nextval('public.item_season_id_seq'::regclass);


--
-- TOC entry 5333 (class 2604 OID 25696)
-- Name: item_season_episode id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_season_episode ALTER COLUMN id SET DEFAULT nextval('public.item_season_episode_id_seq'::regclass);


--
-- TOC entry 5334 (class 2604 OID 25713)
-- Name: item_social_interact id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_social_interact ALTER COLUMN id SET DEFAULT nextval('public.item_social_interact_id_seq'::regclass);


--
-- TOC entry 5335 (class 2604 OID 25728)
-- Name: item_soundbite id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_soundbite ALTER COLUMN id SET DEFAULT nextval('public.item_soundbite_id_seq'::regclass);


--
-- TOC entry 5336 (class 2604 OID 25745)
-- Name: item_transcript id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_transcript ALTER COLUMN id SET DEFAULT nextval('public.item_transcript_id_seq'::regclass);


--
-- TOC entry 5337 (class 2604 OID 25761)
-- Name: item_txt id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_txt ALTER COLUMN id SET DEFAULT nextval('public.item_txt_id_seq'::regclass);


--
-- TOC entry 5338 (class 2604 OID 25776)
-- Name: item_value id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_value ALTER COLUMN id SET DEFAULT nextval('public.item_value_id_seq'::regclass);


--
-- TOC entry 5339 (class 2604 OID 25791)
-- Name: item_value_recipient id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_value_recipient ALTER COLUMN id SET DEFAULT nextval('public.item_value_recipient_id_seq'::regclass);


--
-- TOC entry 5341 (class 2604 OID 25807)
-- Name: item_value_time_split id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_value_time_split ALTER COLUMN id SET DEFAULT nextval('public.item_value_time_split_id_seq'::regclass);


--
-- TOC entry 5345 (class 2604 OID 25844)
-- Name: item_value_time_split_recipient id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_value_time_split_recipient ALTER COLUMN id SET DEFAULT nextval('public.item_value_time_split_recipient_id_seq'::regclass);


--
-- TOC entry 5344 (class 2604 OID 25824)
-- Name: item_value_time_split_remote_item id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_value_time_split_remote_item ALTER COLUMN id SET DEFAULT nextval('public.item_value_time_split_remote_item_id_seq'::regclass);


--
-- TOC entry 5348 (class 2604 OID 25872)
-- Name: live_item id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.live_item ALTER COLUMN id SET DEFAULT nextval('public.live_item_id_seq'::regclass);


--
-- TOC entry 5347 (class 2604 OID 25860)
-- Name: live_item_status id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.live_item_status ALTER COLUMN id SET DEFAULT nextval('public.live_item_status_id_seq'::regclass);


--
-- TOC entry 5274 (class 2604 OID 24867)
-- Name: medium id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medium ALTER COLUMN id SET DEFAULT nextval('public.medium_id_seq'::regclass);


--
-- TOC entry 5363 (class 2604 OID 26091)
-- Name: playlist id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.playlist ALTER COLUMN id SET DEFAULT nextval('public.playlist_id_seq'::regclass);


--
-- TOC entry 5366 (class 2604 OID 26123)
-- Name: playlist_resource id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.playlist_resource ALTER COLUMN id SET DEFAULT nextval('public.playlist_resource_id_seq'::regclass);


--
-- TOC entry 5367 (class 2604 OID 26178)
-- Name: queue id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.queue ALTER COLUMN id SET DEFAULT nextval('public.queue_id_seq'::regclass);


--
-- TOC entry 5368 (class 2604 OID 26203)
-- Name: queue_resource id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.queue_resource ALTER COLUMN id SET DEFAULT nextval('public.queue_resource_id_seq'::regclass);


--
-- TOC entry 5349 (class 2604 OID 25895)
-- Name: sharable_status id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sharable_status ALTER COLUMN id SET DEFAULT nextval('public.sharable_status_id_seq'::regclass);


--
-- TOC entry 5455 (class 2604 OID 26704)
-- Name: stats_aggregated_account id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_aggregated_account ALTER COLUMN id SET DEFAULT nextval('public.stats_aggregated_account_id_seq'::regclass);


--
-- TOC entry 5379 (class 2604 OID 26472)
-- Name: stats_aggregated_channel id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_aggregated_channel ALTER COLUMN id SET DEFAULT nextval('public.stats_aggregated_channel_id_seq'::regclass);


--
-- TOC entry 5417 (class 2604 OID 26588)
-- Name: stats_aggregated_clip id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_aggregated_clip ALTER COLUMN id SET DEFAULT nextval('public.stats_aggregated_clip_id_seq'::regclass);


--
-- TOC entry 5398 (class 2604 OID 26530)
-- Name: stats_aggregated_item id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_aggregated_item ALTER COLUMN id SET DEFAULT nextval('public.stats_aggregated_item_id_seq'::regclass);


--
-- TOC entry 5436 (class 2604 OID 26646)
-- Name: stats_aggregated_playlist id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_aggregated_playlist ALTER COLUMN id SET DEFAULT nextval('public.stats_aggregated_playlist_id_seq'::regclass);


--
-- TOC entry 5377 (class 2604 OID 26431)
-- Name: stats_track_account_guid id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_account_guid ALTER COLUMN id SET DEFAULT nextval('public.stats_track_account_guid_id_seq'::regclass);


--
-- TOC entry 5454 (class 2604 OID 26682)
-- Name: stats_track_event_account id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_event_account ALTER COLUMN id SET DEFAULT nextval('public.stats_track_event_account_id_seq'::regclass);


--
-- TOC entry 5378 (class 2604 OID 26450)
-- Name: stats_track_event_channel id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_event_channel ALTER COLUMN id SET DEFAULT nextval('public.stats_track_event_channel_id_seq'::regclass);


--
-- TOC entry 5416 (class 2604 OID 26566)
-- Name: stats_track_event_clip id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_event_clip ALTER COLUMN id SET DEFAULT nextval('public.stats_track_event_clip_id_seq'::regclass);


--
-- TOC entry 5397 (class 2604 OID 26508)
-- Name: stats_track_event_item id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_event_item ALTER COLUMN id SET DEFAULT nextval('public.stats_track_event_item_id_seq'::regclass);


--
-- TOC entry 5435 (class 2604 OID 26624)
-- Name: stats_track_event_playlist id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_event_playlist ALTER COLUMN id SET DEFAULT nextval('public.stats_track_event_playlist_id_seq'::regclass);


--
-- TOC entry 6409 (class 0 OID 25904)
-- Dependencies: 340
-- Data for Name: account; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account (id, id_text, verified, sharable_status_id) FROM stdin;
\.


--
-- TOC entry 6425 (class 0 OID 26042)
-- Dependencies: 356
-- Data for Name: account_admin_roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account_admin_roles (id, account_id, dev_admin, podping_admin) FROM stdin;
\.


--
-- TOC entry 6446 (class 0 OID 26385)
-- Dependencies: 377
-- Data for Name: account_app_store_purchase; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account_app_store_purchase (account_id, transaction_id, cancellation_date, cancellation_date_ms, cancellation_date_pst, cancellation_reason, expires_date, expires_date_ms, expires_date_pst, is_in_intro_offer_period, is_trial_period, original_purchase_date, original_purchase_date_ms, original_purchase_date_pst, original_transaction_id, product_id, promotional_offer_id, purchase_date, purchase_date_ms, purchase_date_pst, quantity, web_order_line_item_id) FROM stdin;
\.


--
-- TOC entry 6411 (class 0 OID 25922)
-- Dependencies: 342
-- Data for Name: account_credentials; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account_credentials (id, account_id, email, password) FROM stdin;
\.


--
-- TOC entry 6419 (class 0 OID 25992)
-- Dependencies: 350
-- Data for Name: account_email_change_verification; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account_email_change_verification (id, account_id, verification_token, verification_token_expires_at, pending_email_address) FROM stdin;
\.


--
-- TOC entry 6444 (class 0 OID 26355)
-- Dependencies: 375
-- Data for Name: account_fcm_device; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account_fcm_device (id, fcm_token, account_id) FROM stdin;
\.


--
-- TOC entry 6436 (class 0 OID 26255)
-- Dependencies: 367
-- Data for Name: account_following_account; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account_following_account (account_id, following_account_id) FROM stdin;
\.


--
-- TOC entry 6439 (class 0 OID 26306)
-- Dependencies: 370
-- Data for Name: account_following_add_by_rss_channel; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account_following_add_by_rss_channel (account_id, feed_url, title, image_url) FROM stdin;
\.


--
-- TOC entry 6437 (class 0 OID 26272)
-- Dependencies: 368
-- Data for Name: account_following_channel; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account_following_channel (account_id, channel_id) FROM stdin;
\.


--
-- TOC entry 6438 (class 0 OID 26289)
-- Dependencies: 369
-- Data for Name: account_following_playlist; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account_following_playlist (account_id, playlist_id) FROM stdin;
\.


--
-- TOC entry 6447 (class 0 OID 26398)
-- Dependencies: 378
-- Data for Name: account_google_play_purchase; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account_google_play_purchase (account_id, transaction_id, acknowledgement_state, consumption_state, developer_payload, kind, product_id, purchase_time_millis, purchase_state, purchase_token) FROM stdin;
\.


--
-- TOC entry 6421 (class 0 OID 26009)
-- Dependencies: 352
-- Data for Name: account_membership; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account_membership (id, tier) FROM stdin;
1	trial
2	basic
\.


--
-- TOC entry 6423 (class 0 OID 26021)
-- Dependencies: 354
-- Data for Name: account_membership_status; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account_membership_status (id, account_id, account_membership_id, membership_expires_at) FROM stdin;
\.


--
-- TOC entry 6440 (class 0 OID 26319)
-- Dependencies: 371
-- Data for Name: account_notification_channel; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account_notification_channel (channel_id, account_id) FROM stdin;
\.


--
-- TOC entry 6445 (class 0 OID 26372)
-- Dependencies: 376
-- Data for Name: account_paypal_order; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account_paypal_order (account_id, payment_id, state) FROM stdin;
\.


--
-- TOC entry 6413 (class 0 OID 25941)
-- Dependencies: 344
-- Data for Name: account_profile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account_profile (id, account_id, display_name, bio) FROM stdin;
\.


--
-- TOC entry 6415 (class 0 OID 25958)
-- Dependencies: 346
-- Data for Name: account_reset_password; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account_reset_password (id, account_id, reset_token, reset_token_expires_at) FROM stdin;
\.


--
-- TOC entry 6442 (class 0 OID 26337)
-- Dependencies: 373
-- Data for Name: account_up_device; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account_up_device (id, account_id, up_endpoint, up_public_key, up_auth_key) FROM stdin;
\.


--
-- TOC entry 6417 (class 0 OID 25975)
-- Dependencies: 348
-- Data for Name: account_verification; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account_verification (id, account_id, verification_token, verification_token_expires_at) FROM stdin;
\.


--
-- TOC entry 6287 (class 0 OID 24849)
-- Dependencies: 218
-- Data for Name: category; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.category (id, parent_id, display_name, slug, mapping_key) FROM stdin;
1	\N	Arts	arts	arts
2	\N	Business	business	business
3	\N	Comedy	comedy	comedy
4	\N	Education	education	education
5	\N	Fiction	fiction	fiction
6	\N	Government	government	government
7	\N	History	history	history
8	\N	Health & Fitness	health-and-fitness	healthandfitness
9	\N	Kids & Family	kids-and-family	kidsandfamily
10	\N	Leisure	leisure	leisure
11	\N	Music	music	music
12	\N	News	news	news
13	\N	Religion & Spirituality	religion-and-spirituality	religionandspirituality
14	\N	Science	science	science
15	\N	Society & Culture	society-and-culture	societyandculture
16	\N	Sports	sports	sports
17	\N	Technology	technology	technology
18	\N	True Crime	true-crime	truecrime
19	\N	TV & Film	tv-and-film	tvandfilm
20	1	Books	books	books
21	1	Design	design	design
22	1	Fashion & Beauty	fashion-and-beauty	fashionandbeauty
23	1	Food	food	food
24	1	Performing Arts	performing-arts	performingarts
25	1	Visual Arts	visual-arts	visualarts
26	2	Careers	careers	careers
27	2	Entrepreneurship	entrepreneurship	entrepreneurship
28	2	Investing	investing	investing
29	2	Management	management	management
30	2	Marketing	marketing	marketing
31	2	Non-Profit	non-profit	nonprofit
32	3	Comedy Interviews	comedy-interviews	comedyinterviews
33	3	Improv	improv	improv
34	3	Stand-Up	stand-up	standup
35	4	Courses	courses	courses
36	4	How To	how-to	howto
37	4	Language Learning	language-learning	languagelearning
38	4	Self-Improvement	self-improvement	selfimprovement
39	5	Comedy Fiction	comedy-fiction	comedyfiction
40	5	Drama	drama	drama
41	5	Science Fiction	science-fiction	sciencefiction
42	8	Alternative Health	alternative-health	alternativehealth
43	8	Fitness	fitness	fitness
44	8	Medicine	medicine	medicine
45	8	Mental Health	mental-health	mentalhealth
46	8	Nutrition	nutrition	nutrition
47	8	Sexuality	sexuality	sexuality
48	9	Education for Kids	education-for-kids	educationforkids
49	9	Parenting	parenting	parenting
50	9	Pets & Animals	pets-and-animals	petsandanimals
51	9	Stories for Kids	stories-for-kids	storiesforkids
52	10	Animation & Manga	animation-and-manga	animationandmanga
53	10	Automotive	automotive	automotive
54	10	Aviation	aviation	aviation
55	10	Crafts	crafts	crafts
56	10	Games	games	games
57	10	Hobbies	hobbies	hobbies
58	10	Home & Garden	home-and-garden	homeandgarden
59	10	Video Games	video-games	videogames
60	11	Music Commentary	music-commentary	musiccommentary
61	11	Music History	music-history	musichistory
62	11	Music Interviews	music-interviews	musicinterviews
63	12	Business News	business-news	businessnews
64	12	Daily News	daily-news	dailynews
65	12	Entertainment News	entertainment-news	entertainmentnews
66	12	News Commentary	news-commentary	newscommentary
67	12	Politics	politics	politics
68	12	Sports News	sports-news	sportsnews
69	12	Tech News	tech-news	technews
70	13	Buddhism	buddhism	buddhism
71	13	Christianity	christianity	christianity
72	13	Hinduism	hinduism	hinduism
73	13	Islam	islam	islam
74	13	Judaism	judaism	judaism
75	13	Religion	religion	religion
76	13	Spirituality	spirituality	spirituality
77	14	Astronomy	astronomy	astronomy
78	14	Chemistry	chemistry	chemistry
79	14	Earth Sciences	earth-sciences	earthsciences
80	14	Life Sciences	life-sciences	lifesciences
81	14	Mathematics	mathematics	mathematics
82	14	Natural Sciences	natural-sciences	naturalsciences
83	14	Nature	nature	nature
84	14	Physics	physics	physics
85	14	Social Sciences	social-sciences	socialsciences
86	15	Documentary	documentary	documentary
87	15	Personal Journals	personal-journals	personaljournals
88	15	Philosophy	philosophy	philosophy
89	15	Places & Travel	places-and-travel	placesandtravel
90	15	Relationships	relationships	relationships
91	16	Baseball	baseball	baseball
92	16	Basketball	basketball	basketball
93	16	Cricket	cricket	cricket
94	16	Fantasy Sports	fantasy-sports	fantasysports
95	16	Football	football	football
96	16	Golf	golf	golf
97	16	Hockey	hockey	hockey
98	16	Rugby	rugby	rugby
99	16	Running	running	running
100	16	Soccer	soccer	soccer
101	16	Swimming	swimming	swimming
102	16	Tennis	tennis	tennis
103	16	Volleyball	volleyball	volleyball
104	16	Wilderness	wilderness	wilderness
105	16	Wrestling	wrestling	wrestling
106	19	After Shows	after-shows	aftershows
107	19	Film History	film-history	filmhistory
108	19	Film Interviews	film-interviews	filminterviews
109	19	Film Reviews	film-reviews	filmreviews
110	19	TV Reviews	tv-reviews	tvreviews
\.


--
-- TOC entry 6297 (class 0 OID 24925)
-- Dependencies: 228
-- Data for Name: channel; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.channel (id, id_text, slug, feed_id, podcast_index_id, podcast_guid, title, sortable_title, medium_id, has_podcast_index_value, has_value_time_splits) FROM stdin;
\.


--
-- TOC entry 6301 (class 0 OID 24970)
-- Dependencies: 232
-- Data for Name: channel_about; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.channel_about (id, channel_id, author, episode_count, explicit, itunes_type_id, language, last_pub_date, website_link_url) FROM stdin;
\.


--
-- TOC entry 6303 (class 0 OID 24993)
-- Dependencies: 234
-- Data for Name: channel_category; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.channel_category (id, channel_id, category_id) FROM stdin;
\.


--
-- TOC entry 6305 (class 0 OID 25012)
-- Dependencies: 236
-- Data for Name: channel_chat; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.channel_chat (id, channel_id, server, protocol, account_id, space) FROM stdin;
\.


--
-- TOC entry 6307 (class 0 OID 25029)
-- Dependencies: 238
-- Data for Name: channel_description; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.channel_description (id, channel_id, value) FROM stdin;
\.


--
-- TOC entry 6309 (class 0 OID 25046)
-- Dependencies: 240
-- Data for Name: channel_funding; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.channel_funding (id, channel_id, url, title) FROM stdin;
\.


--
-- TOC entry 6311 (class 0 OID 25061)
-- Dependencies: 242
-- Data for Name: channel_image; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.channel_image (id, channel_id, url, image_width_size, is_resized) FROM stdin;
\.


--
-- TOC entry 6313 (class 0 OID 25077)
-- Dependencies: 244
-- Data for Name: channel_internal_settings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.channel_internal_settings (id, channel_id, embed_approved_media_url_paths) FROM stdin;
\.


--
-- TOC entry 6299 (class 0 OID 24958)
-- Dependencies: 230
-- Data for Name: channel_itunes_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.channel_itunes_type (id, itunes_type) FROM stdin;
1	episodic
2	serial
\.


--
-- TOC entry 6315 (class 0 OID 25092)
-- Dependencies: 246
-- Data for Name: channel_license; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.channel_license (id, channel_id, identifier, url) FROM stdin;
\.


--
-- TOC entry 6317 (class 0 OID 25109)
-- Dependencies: 248
-- Data for Name: channel_location; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.channel_location (id, channel_id, geo, osm, name) FROM stdin;
\.


--
-- TOC entry 6319 (class 0 OID 25127)
-- Dependencies: 250
-- Data for Name: channel_person; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.channel_person (id, channel_id, name, role, person_group, img, href) FROM stdin;
\.


--
-- TOC entry 6321 (class 0 OID 25143)
-- Dependencies: 252
-- Data for Name: channel_podroll; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.channel_podroll (id, channel_id) FROM stdin;
\.


--
-- TOC entry 6323 (class 0 OID 25158)
-- Dependencies: 254
-- Data for Name: channel_podroll_remote_item; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.channel_podroll_remote_item (id, channel_podroll_id, feed_guid, feed_url, item_guid, title, medium_id) FROM stdin;
\.


--
-- TOC entry 6325 (class 0 OID 25182)
-- Dependencies: 256
-- Data for Name: channel_publisher; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.channel_publisher (id, channel_id) FROM stdin;
\.


--
-- TOC entry 6327 (class 0 OID 25197)
-- Dependencies: 258
-- Data for Name: channel_publisher_remote_item; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.channel_publisher_remote_item (id, channel_publisher_id, feed_guid, feed_url, item_guid, title, medium_id) FROM stdin;
\.


--
-- TOC entry 6329 (class 0 OID 25223)
-- Dependencies: 260
-- Data for Name: channel_remote_item; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.channel_remote_item (id, channel_id, feed_guid, feed_url, item_guid, title, medium_id) FROM stdin;
\.


--
-- TOC entry 6331 (class 0 OID 25247)
-- Dependencies: 262
-- Data for Name: channel_season; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.channel_season (id, channel_id, number, name) FROM stdin;
\.


--
-- TOC entry 6333 (class 0 OID 25264)
-- Dependencies: 264
-- Data for Name: channel_social_interact; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.channel_social_interact (id, channel_id, protocol, uri, account_id, account_url, priority) FROM stdin;
\.


--
-- TOC entry 6335 (class 0 OID 25279)
-- Dependencies: 266
-- Data for Name: channel_trailer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.channel_trailer (id, channel_id, url, title, pub_date, length, type, channel_season_id) FROM stdin;
\.


--
-- TOC entry 6337 (class 0 OID 25302)
-- Dependencies: 268
-- Data for Name: channel_txt; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.channel_txt (id, channel_id, purpose, value) FROM stdin;
\.


--
-- TOC entry 6339 (class 0 OID 25317)
-- Dependencies: 270
-- Data for Name: channel_value; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.channel_value (id, channel_id, type, method, suggested) FROM stdin;
\.


--
-- TOC entry 6341 (class 0 OID 25332)
-- Dependencies: 272
-- Data for Name: channel_value_recipient; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.channel_value_recipient (id, channel_value_id, type, address, split, name, custom_key, custom_value, fee) FROM stdin;
\.


--
-- TOC entry 6427 (class 0 OID 26059)
-- Dependencies: 358
-- Data for Name: clip; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clip (id, id_text, account_id, item_id, start_time, end_time, title, description, sharable_status_id) FROM stdin;
\.


--
-- TOC entry 6293 (class 0 OID 24889)
-- Dependencies: 224
-- Data for Name: feed; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.feed (id, url, feed_flag_status_id, is_parsing, parsing_priority, last_parsed_file_hash, container_id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 6291 (class 0 OID 24876)
-- Dependencies: 222
-- Data for Name: feed_flag_status; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.feed_flag_status (id, status, created_at, updated_at) FROM stdin;
1	active	2025-06-01 15:09:38.266734	2025-06-01 15:09:38.266734
2	always-parse	2025-06-01 15:09:38.266734	2025-06-01 15:09:38.266734
3	spam	2025-06-01 15:09:38.266734	2025-06-01 15:09:38.266734
4	pending-archive	2025-06-01 15:09:38.266734	2025-06-01 15:09:38.266734
5	archived	2025-06-01 15:09:38.266734	2025-06-01 15:09:38.266734
6	takedown	2025-06-01 15:09:38.266734	2025-06-01 15:09:38.266734
\.


--
-- TOC entry 6295 (class 0 OID 24909)
-- Dependencies: 226
-- Data for Name: feed_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.feed_log (id, feed_id, last_http_status, last_good_http_status_time, last_finished_parse_time, parse_errors) FROM stdin;
\.


--
-- TOC entry 6345 (class 0 OID 25361)
-- Dependencies: 276
-- Data for Name: item; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item (id, id_text, slug, channel_id, guid, guid_enclosure_url, pub_date, title, item_flag_status_id) FROM stdin;
\.


--
-- TOC entry 6349 (class 0 OID 25400)
-- Dependencies: 280
-- Data for Name: item_about; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_about (id, item_id, duration, explicit, website_link_url, item_itunes_episode_type_id) FROM stdin;
\.


--
-- TOC entry 6355 (class 0 OID 25456)
-- Dependencies: 286
-- Data for Name: item_chapter; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_chapter (id, id_text, item_chapters_feed_id, start_time, end_time, title, img, web_url, table_of_contents) FROM stdin;
\.


--
-- TOC entry 6357 (class 0 OID 25474)
-- Dependencies: 288
-- Data for Name: item_chapter_location; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_chapter_location (id, item_chapter_id, geo, osm, name) FROM stdin;
\.


--
-- TOC entry 6351 (class 0 OID 25423)
-- Dependencies: 282
-- Data for Name: item_chapters_feed; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_chapters_feed (id, item_id, url, type) FROM stdin;
\.


--
-- TOC entry 6353 (class 0 OID 25440)
-- Dependencies: 284
-- Data for Name: item_chapters_feed_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_chapters_feed_log (id, item_chapters_feed_id, last_http_status, last_good_http_status_time, last_finished_parse_time, parse_errors) FROM stdin;
\.


--
-- TOC entry 6359 (class 0 OID 25492)
-- Dependencies: 290
-- Data for Name: item_chat; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_chat (id, item_id, server, protocol, account_id, space) FROM stdin;
\.


--
-- TOC entry 6361 (class 0 OID 25509)
-- Dependencies: 292
-- Data for Name: item_content_link; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_content_link (id, item_id, href, title) FROM stdin;
\.


--
-- TOC entry 6363 (class 0 OID 25524)
-- Dependencies: 294
-- Data for Name: item_description; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_description (id, item_id, value) FROM stdin;
\.


--
-- TOC entry 6365 (class 0 OID 25541)
-- Dependencies: 296
-- Data for Name: item_enclosure; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_enclosure (id, item_id, type, length, bitrate, height, language, title, rel, codecs, item_enclosure_default) FROM stdin;
\.


--
-- TOC entry 6369 (class 0 OID 25572)
-- Dependencies: 300
-- Data for Name: item_enclosure_integrity; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_enclosure_integrity (id, item_enclosure_id, type, value) FROM stdin;
\.


--
-- TOC entry 6367 (class 0 OID 25557)
-- Dependencies: 298
-- Data for Name: item_enclosure_source; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_enclosure_source (id, item_enclosure_id, uri, content_type) FROM stdin;
\.


--
-- TOC entry 6343 (class 0 OID 25348)
-- Dependencies: 274
-- Data for Name: item_flag_status; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_flag_status (id, status, created_at, updated_at) FROM stdin;
1	active	2025-06-01 15:09:38.406506	2025-06-01 15:09:38.406506
2	pending-archive	2025-06-01 15:09:38.406506	2025-06-01 15:09:38.406506
3	archived	2025-06-01 15:09:38.406506	2025-06-01 15:09:38.406506
4	pending-delete	2025-06-01 15:09:38.406506	2025-06-01 15:09:38.406506
\.


--
-- TOC entry 6371 (class 0 OID 25590)
-- Dependencies: 302
-- Data for Name: item_funding; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_funding (id, item_id, url, title) FROM stdin;
\.


--
-- TOC entry 6373 (class 0 OID 25605)
-- Dependencies: 304
-- Data for Name: item_image; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_image (id, item_id, url, image_width_size, is_resized) FROM stdin;
\.


--
-- TOC entry 6347 (class 0 OID 25388)
-- Dependencies: 278
-- Data for Name: item_itunes_episode_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_itunes_episode_type (id, itunes_episode_type) FROM stdin;
1	full
2	trailer
3	bonus
\.


--
-- TOC entry 6375 (class 0 OID 25621)
-- Dependencies: 306
-- Data for Name: item_license; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_license (id, item_id, identifier, url) FROM stdin;
\.


--
-- TOC entry 6377 (class 0 OID 25638)
-- Dependencies: 308
-- Data for Name: item_location; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_location (id, item_id, geo, osm, name) FROM stdin;
\.


--
-- TOC entry 6379 (class 0 OID 25656)
-- Dependencies: 310
-- Data for Name: item_person; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_person (id, item_id, name, role, person_group, img, href) FROM stdin;
\.


--
-- TOC entry 6381 (class 0 OID 25672)
-- Dependencies: 312
-- Data for Name: item_season; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_season (id, channel_season_id, item_id, title) FROM stdin;
\.


--
-- TOC entry 6383 (class 0 OID 25693)
-- Dependencies: 314
-- Data for Name: item_season_episode; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_season_episode (id, item_id, display, number) FROM stdin;
\.


--
-- TOC entry 6385 (class 0 OID 25710)
-- Dependencies: 316
-- Data for Name: item_social_interact; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_social_interact (id, item_id, protocol, uri, account_id, account_url, priority) FROM stdin;
\.


--
-- TOC entry 6387 (class 0 OID 25725)
-- Dependencies: 318
-- Data for Name: item_soundbite; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_soundbite (id, id_text, item_id, start_time, duration, title) FROM stdin;
\.


--
-- TOC entry 6389 (class 0 OID 25742)
-- Dependencies: 320
-- Data for Name: item_transcript; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_transcript (id, item_id, url, type, language, rel) FROM stdin;
\.


--
-- TOC entry 6391 (class 0 OID 25758)
-- Dependencies: 322
-- Data for Name: item_txt; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_txt (id, item_id, purpose, value) FROM stdin;
\.


--
-- TOC entry 6393 (class 0 OID 25773)
-- Dependencies: 324
-- Data for Name: item_value; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_value (id, item_id, type, method, suggested) FROM stdin;
\.


--
-- TOC entry 6395 (class 0 OID 25788)
-- Dependencies: 326
-- Data for Name: item_value_recipient; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_value_recipient (id, item_value_id, type, address, split, name, custom_key, custom_value, fee) FROM stdin;
\.


--
-- TOC entry 6397 (class 0 OID 25804)
-- Dependencies: 328
-- Data for Name: item_value_time_split; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_value_time_split (id, item_value_id, start_time, duration, remote_start_time, remote_percentage) FROM stdin;
\.


--
-- TOC entry 6401 (class 0 OID 25841)
-- Dependencies: 332
-- Data for Name: item_value_time_split_recipient; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_value_time_split_recipient (id, item_value_time_split_id, type, address, split, name, custom_key, custom_value, fee) FROM stdin;
\.


--
-- TOC entry 6399 (class 0 OID 25821)
-- Dependencies: 330
-- Data for Name: item_value_time_split_remote_item; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_value_time_split_remote_item (id, item_value_time_split_id, feed_guid, feed_url, item_guid, title) FROM stdin;
\.


--
-- TOC entry 6405 (class 0 OID 25869)
-- Dependencies: 336
-- Data for Name: live_item; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.live_item (id, item_id, live_item_status_id, start_time, end_time, chat_web_url) FROM stdin;
\.


--
-- TOC entry 6403 (class 0 OID 25857)
-- Dependencies: 334
-- Data for Name: live_item_status; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.live_item_status (id, status) FROM stdin;
1	pending
2	live
3	ended
\.


--
-- TOC entry 6289 (class 0 OID 24864)
-- Dependencies: 220
-- Data for Name: medium; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.medium (id, value) FROM stdin;
1	publisher
2	podcast
3	music
4	video
5	film
6	audiobook
7	newsletter
8	blog
9	course
10	mixed
11	podcastL
12	musicL
13	videoL
14	filmL
15	audiobookL
16	newsletterL
17	blogL
18	publisherL
19	courseL
\.


--
-- TOC entry 6448 (class 0 OID 26413)
-- Dependencies: 379
-- Data for Name: membership_claim_token; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.membership_claim_token (id, claimed, months_to_add, account_membership_id) FROM stdin;
\.


--
-- TOC entry 6429 (class 0 OID 26088)
-- Dependencies: 360
-- Data for Name: playlist; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.playlist (id, id_text, account_id, sharable_status_id, title, description, is_default_favorites, item_count, medium_id) FROM stdin;
\.


--
-- TOC entry 6431 (class 0 OID 26120)
-- Dependencies: 362
-- Data for Name: playlist_resource; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.playlist_resource (id, playlist_id, list_position, item_id, item_chapter_id, clip_id, item_soundbite_id, add_by_rss_resource_data, add_by_rss_hash_id) FROM stdin;
\.


--
-- TOC entry 6433 (class 0 OID 26175)
-- Dependencies: 364
-- Data for Name: queue; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.queue (id, id_text, account_id, medium_id) FROM stdin;
\.


--
-- TOC entry 6435 (class 0 OID 26200)
-- Dependencies: 366
-- Data for Name: queue_resource; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.queue_resource (id, queue_id, list_position, playback_position, media_file_duration, completed, item_id, item_chapter_id, clip_id, item_soundbite_id, add_by_rss_resource_data, add_by_rss_hash_id) FROM stdin;
\.


--
-- TOC entry 6407 (class 0 OID 25892)
-- Dependencies: 338
-- Data for Name: sharable_status; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sharable_status (id, status) FROM stdin;
1	public
2	unlisted
3	private
\.


--
-- TOC entry 6470 (class 0 OID 26701)
-- Dependencies: 401
-- Data for Name: stats_aggregated_account; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stats_aggregated_account (id, tracked_account_id, day_current_count, day_1_count, day_2_count, day_3_count, day_4_count, day_5_count, day_6_count, day_7_count, day_8_count, week_current_count, week_1_count, week_2_count, week_3_count, week_4_count, month_current_count, month_1_count, all_time_count) FROM stdin;
\.


--
-- TOC entry 6454 (class 0 OID 26469)
-- Dependencies: 385
-- Data for Name: stats_aggregated_channel; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stats_aggregated_channel (id, channel_id, day_current_count, day_1_count, day_2_count, day_3_count, day_4_count, day_5_count, day_6_count, day_7_count, day_8_count, week_current_count, week_1_count, week_2_count, week_3_count, week_4_count, month_current_count, month_1_count, all_time_count) FROM stdin;
\.


--
-- TOC entry 6462 (class 0 OID 26585)
-- Dependencies: 393
-- Data for Name: stats_aggregated_clip; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stats_aggregated_clip (id, clip_id, day_current_count, day_1_count, day_2_count, day_3_count, day_4_count, day_5_count, day_6_count, day_7_count, day_8_count, week_current_count, week_1_count, week_2_count, week_3_count, week_4_count, month_current_count, month_1_count, all_time_count) FROM stdin;
\.


--
-- TOC entry 6458 (class 0 OID 26527)
-- Dependencies: 389
-- Data for Name: stats_aggregated_item; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stats_aggregated_item (id, item_id, day_current_count, day_1_count, day_2_count, day_3_count, day_4_count, day_5_count, day_6_count, day_7_count, day_8_count, week_current_count, week_1_count, week_2_count, week_3_count, week_4_count, month_current_count, month_1_count, all_time_count) FROM stdin;
\.


--
-- TOC entry 6466 (class 0 OID 26643)
-- Dependencies: 397
-- Data for Name: stats_aggregated_playlist; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stats_aggregated_playlist (id, playlist_id, day_current_count, day_1_count, day_2_count, day_3_count, day_4_count, day_5_count, day_6_count, day_7_count, day_8_count, week_current_count, week_1_count, week_2_count, week_3_count, week_4_count, month_current_count, month_1_count, all_time_count) FROM stdin;
\.


--
-- TOC entry 6450 (class 0 OID 26428)
-- Dependencies: 381
-- Data for Name: stats_track_account_guid; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stats_track_account_guid (id, account_id, account_guid, updated_at) FROM stdin;
\.


--
-- TOC entry 6468 (class 0 OID 26679)
-- Dependencies: 399
-- Data for Name: stats_track_event_account; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stats_track_event_account (id, account_guid, tracked_account_id, created_at) FROM stdin;
\.


--
-- TOC entry 6452 (class 0 OID 26447)
-- Dependencies: 383
-- Data for Name: stats_track_event_channel; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stats_track_event_channel (id, account_guid, channel_id, created_at) FROM stdin;
\.


--
-- TOC entry 6460 (class 0 OID 26563)
-- Dependencies: 391
-- Data for Name: stats_track_event_clip; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stats_track_event_clip (id, account_guid, clip_id, created_at) FROM stdin;
\.


--
-- TOC entry 6456 (class 0 OID 26505)
-- Dependencies: 387
-- Data for Name: stats_track_event_item; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stats_track_event_item (id, account_guid, item_id, created_at) FROM stdin;
\.


--
-- TOC entry 6464 (class 0 OID 26621)
-- Dependencies: 395
-- Data for Name: stats_track_event_playlist; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stats_track_event_playlist (id, account_guid, playlist_id, created_at) FROM stdin;
\.


--
-- TOC entry 6750 (class 0 OID 0)
-- Dependencies: 355
-- Name: account_admin_roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.account_admin_roles_id_seq', 1, false);


--
-- TOC entry 6751 (class 0 OID 0)
-- Dependencies: 341
-- Name: account_credentials_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.account_credentials_id_seq', 1, false);


--
-- TOC entry 6752 (class 0 OID 0)
-- Dependencies: 349
-- Name: account_email_change_verification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.account_email_change_verification_id_seq', 1, false);


--
-- TOC entry 6753 (class 0 OID 0)
-- Dependencies: 374
-- Name: account_fcm_device_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.account_fcm_device_id_seq', 1, false);


--
-- TOC entry 6754 (class 0 OID 0)
-- Dependencies: 339
-- Name: account_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.account_id_seq', 1, false);


--
-- TOC entry 6755 (class 0 OID 0)
-- Dependencies: 351
-- Name: account_membership_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.account_membership_id_seq', 2, true);


--
-- TOC entry 6756 (class 0 OID 0)
-- Dependencies: 353
-- Name: account_membership_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.account_membership_status_id_seq', 1, false);


--
-- TOC entry 6757 (class 0 OID 0)
-- Dependencies: 343
-- Name: account_profile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.account_profile_id_seq', 1, false);


--
-- TOC entry 6758 (class 0 OID 0)
-- Dependencies: 345
-- Name: account_reset_password_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.account_reset_password_id_seq', 1, false);


--
-- TOC entry 6759 (class 0 OID 0)
-- Dependencies: 372
-- Name: account_up_device_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.account_up_device_id_seq', 1, false);


--
-- TOC entry 6760 (class 0 OID 0)
-- Dependencies: 347
-- Name: account_verification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.account_verification_id_seq', 1, false);


--
-- TOC entry 6761 (class 0 OID 0)
-- Dependencies: 217
-- Name: category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.category_id_seq', 110, true);


--
-- TOC entry 6762 (class 0 OID 0)
-- Dependencies: 231
-- Name: channel_about_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.channel_about_id_seq', 1, false);


--
-- TOC entry 6763 (class 0 OID 0)
-- Dependencies: 233
-- Name: channel_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.channel_category_id_seq', 1, false);


--
-- TOC entry 6764 (class 0 OID 0)
-- Dependencies: 235
-- Name: channel_chat_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.channel_chat_id_seq', 1, false);


--
-- TOC entry 6765 (class 0 OID 0)
-- Dependencies: 237
-- Name: channel_description_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.channel_description_id_seq', 1, false);


--
-- TOC entry 6766 (class 0 OID 0)
-- Dependencies: 239
-- Name: channel_funding_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.channel_funding_id_seq', 1, false);


--
-- TOC entry 6767 (class 0 OID 0)
-- Dependencies: 227
-- Name: channel_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.channel_id_seq', 1, false);


--
-- TOC entry 6768 (class 0 OID 0)
-- Dependencies: 241
-- Name: channel_image_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.channel_image_id_seq', 1, false);


--
-- TOC entry 6769 (class 0 OID 0)
-- Dependencies: 243
-- Name: channel_internal_settings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.channel_internal_settings_id_seq', 1, false);


--
-- TOC entry 6770 (class 0 OID 0)
-- Dependencies: 229
-- Name: channel_itunes_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.channel_itunes_type_id_seq', 2, true);


--
-- TOC entry 6771 (class 0 OID 0)
-- Dependencies: 245
-- Name: channel_license_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.channel_license_id_seq', 1, false);


--
-- TOC entry 6772 (class 0 OID 0)
-- Dependencies: 247
-- Name: channel_location_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.channel_location_id_seq', 1, false);


--
-- TOC entry 6773 (class 0 OID 0)
-- Dependencies: 249
-- Name: channel_person_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.channel_person_id_seq', 1, false);


--
-- TOC entry 6774 (class 0 OID 0)
-- Dependencies: 251
-- Name: channel_podroll_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.channel_podroll_id_seq', 1, false);


--
-- TOC entry 6775 (class 0 OID 0)
-- Dependencies: 253
-- Name: channel_podroll_remote_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.channel_podroll_remote_item_id_seq', 1, false);


--
-- TOC entry 6776 (class 0 OID 0)
-- Dependencies: 255
-- Name: channel_publisher_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.channel_publisher_id_seq', 1, false);


--
-- TOC entry 6777 (class 0 OID 0)
-- Dependencies: 257
-- Name: channel_publisher_remote_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.channel_publisher_remote_item_id_seq', 1, false);


--
-- TOC entry 6778 (class 0 OID 0)
-- Dependencies: 259
-- Name: channel_remote_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.channel_remote_item_id_seq', 1, false);


--
-- TOC entry 6779 (class 0 OID 0)
-- Dependencies: 261
-- Name: channel_season_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.channel_season_id_seq', 1, false);


--
-- TOC entry 6780 (class 0 OID 0)
-- Dependencies: 263
-- Name: channel_social_interact_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.channel_social_interact_id_seq', 1, false);


--
-- TOC entry 6781 (class 0 OID 0)
-- Dependencies: 265
-- Name: channel_trailer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.channel_trailer_id_seq', 1, false);


--
-- TOC entry 6782 (class 0 OID 0)
-- Dependencies: 267
-- Name: channel_txt_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.channel_txt_id_seq', 1, false);


--
-- TOC entry 6783 (class 0 OID 0)
-- Dependencies: 269
-- Name: channel_value_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.channel_value_id_seq', 1, false);


--
-- TOC entry 6784 (class 0 OID 0)
-- Dependencies: 271
-- Name: channel_value_recipient_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.channel_value_recipient_id_seq', 1, false);


--
-- TOC entry 6785 (class 0 OID 0)
-- Dependencies: 357
-- Name: clip_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.clip_id_seq', 1, false);


--
-- TOC entry 6786 (class 0 OID 0)
-- Dependencies: 221
-- Name: feed_flag_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.feed_flag_status_id_seq', 6, true);


--
-- TOC entry 6787 (class 0 OID 0)
-- Dependencies: 223
-- Name: feed_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.feed_id_seq', 1, false);


--
-- TOC entry 6788 (class 0 OID 0)
-- Dependencies: 225
-- Name: feed_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.feed_log_id_seq', 1, false);


--
-- TOC entry 6789 (class 0 OID 0)
-- Dependencies: 279
-- Name: item_about_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_about_id_seq', 1, false);


--
-- TOC entry 6790 (class 0 OID 0)
-- Dependencies: 285
-- Name: item_chapter_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_chapter_id_seq', 1, false);


--
-- TOC entry 6791 (class 0 OID 0)
-- Dependencies: 287
-- Name: item_chapter_location_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_chapter_location_id_seq', 1, false);


--
-- TOC entry 6792 (class 0 OID 0)
-- Dependencies: 281
-- Name: item_chapters_feed_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_chapters_feed_id_seq', 1, false);


--
-- TOC entry 6793 (class 0 OID 0)
-- Dependencies: 283
-- Name: item_chapters_feed_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_chapters_feed_log_id_seq', 1, false);


--
-- TOC entry 6794 (class 0 OID 0)
-- Dependencies: 289
-- Name: item_chat_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_chat_id_seq', 1, false);


--
-- TOC entry 6795 (class 0 OID 0)
-- Dependencies: 291
-- Name: item_content_link_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_content_link_id_seq', 1, false);


--
-- TOC entry 6796 (class 0 OID 0)
-- Dependencies: 293
-- Name: item_description_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_description_id_seq', 1, false);


--
-- TOC entry 6797 (class 0 OID 0)
-- Dependencies: 295
-- Name: item_enclosure_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_enclosure_id_seq', 1, false);


--
-- TOC entry 6798 (class 0 OID 0)
-- Dependencies: 299
-- Name: item_enclosure_integrity_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_enclosure_integrity_id_seq', 1, false);


--
-- TOC entry 6799 (class 0 OID 0)
-- Dependencies: 297
-- Name: item_enclosure_source_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_enclosure_source_id_seq', 1, false);


--
-- TOC entry 6800 (class 0 OID 0)
-- Dependencies: 273
-- Name: item_flag_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_flag_status_id_seq', 4, true);


--
-- TOC entry 6801 (class 0 OID 0)
-- Dependencies: 301
-- Name: item_funding_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_funding_id_seq', 1, false);


--
-- TOC entry 6802 (class 0 OID 0)
-- Dependencies: 275
-- Name: item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_id_seq', 1, false);


--
-- TOC entry 6803 (class 0 OID 0)
-- Dependencies: 303
-- Name: item_image_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_image_id_seq', 1, false);


--
-- TOC entry 6804 (class 0 OID 0)
-- Dependencies: 277
-- Name: item_itunes_episode_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_itunes_episode_type_id_seq', 3, true);


--
-- TOC entry 6805 (class 0 OID 0)
-- Dependencies: 305
-- Name: item_license_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_license_id_seq', 1, false);


--
-- TOC entry 6806 (class 0 OID 0)
-- Dependencies: 307
-- Name: item_location_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_location_id_seq', 1, false);


--
-- TOC entry 6807 (class 0 OID 0)
-- Dependencies: 309
-- Name: item_person_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_person_id_seq', 1, false);


--
-- TOC entry 6808 (class 0 OID 0)
-- Dependencies: 313
-- Name: item_season_episode_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_season_episode_id_seq', 1, false);


--
-- TOC entry 6809 (class 0 OID 0)
-- Dependencies: 311
-- Name: item_season_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_season_id_seq', 1, false);


--
-- TOC entry 6810 (class 0 OID 0)
-- Dependencies: 315
-- Name: item_social_interact_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_social_interact_id_seq', 1, false);


--
-- TOC entry 6811 (class 0 OID 0)
-- Dependencies: 317
-- Name: item_soundbite_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_soundbite_id_seq', 1, false);


--
-- TOC entry 6812 (class 0 OID 0)
-- Dependencies: 319
-- Name: item_transcript_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_transcript_id_seq', 1, false);


--
-- TOC entry 6813 (class 0 OID 0)
-- Dependencies: 321
-- Name: item_txt_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_txt_id_seq', 1, false);


--
-- TOC entry 6814 (class 0 OID 0)
-- Dependencies: 323
-- Name: item_value_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_value_id_seq', 1, false);


--
-- TOC entry 6815 (class 0 OID 0)
-- Dependencies: 325
-- Name: item_value_recipient_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_value_recipient_id_seq', 1, false);


--
-- TOC entry 6816 (class 0 OID 0)
-- Dependencies: 327
-- Name: item_value_time_split_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_value_time_split_id_seq', 1, false);


--
-- TOC entry 6817 (class 0 OID 0)
-- Dependencies: 331
-- Name: item_value_time_split_recipient_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_value_time_split_recipient_id_seq', 1, false);


--
-- TOC entry 6818 (class 0 OID 0)
-- Dependencies: 329
-- Name: item_value_time_split_remote_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_value_time_split_remote_item_id_seq', 1, false);


--
-- TOC entry 6819 (class 0 OID 0)
-- Dependencies: 335
-- Name: live_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.live_item_id_seq', 1, false);


--
-- TOC entry 6820 (class 0 OID 0)
-- Dependencies: 333
-- Name: live_item_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.live_item_status_id_seq', 3, true);


--
-- TOC entry 6821 (class 0 OID 0)
-- Dependencies: 219
-- Name: medium_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.medium_id_seq', 19, true);


--
-- TOC entry 6822 (class 0 OID 0)
-- Dependencies: 359
-- Name: playlist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.playlist_id_seq', 1, false);


--
-- TOC entry 6823 (class 0 OID 0)
-- Dependencies: 361
-- Name: playlist_resource_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.playlist_resource_id_seq', 1, false);


--
-- TOC entry 6824 (class 0 OID 0)
-- Dependencies: 363
-- Name: queue_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.queue_id_seq', 1, false);


--
-- TOC entry 6825 (class 0 OID 0)
-- Dependencies: 365
-- Name: queue_resource_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.queue_resource_id_seq', 1, false);


--
-- TOC entry 6826 (class 0 OID 0)
-- Dependencies: 337
-- Name: sharable_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sharable_status_id_seq', 3, true);


--
-- TOC entry 6827 (class 0 OID 0)
-- Dependencies: 400
-- Name: stats_aggregated_account_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.stats_aggregated_account_id_seq', 1, false);


--
-- TOC entry 6828 (class 0 OID 0)
-- Dependencies: 384
-- Name: stats_aggregated_channel_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.stats_aggregated_channel_id_seq', 1, false);


--
-- TOC entry 6829 (class 0 OID 0)
-- Dependencies: 392
-- Name: stats_aggregated_clip_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.stats_aggregated_clip_id_seq', 1, false);


--
-- TOC entry 6830 (class 0 OID 0)
-- Dependencies: 388
-- Name: stats_aggregated_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.stats_aggregated_item_id_seq', 1, false);


--
-- TOC entry 6831 (class 0 OID 0)
-- Dependencies: 396
-- Name: stats_aggregated_playlist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.stats_aggregated_playlist_id_seq', 1, false);


--
-- TOC entry 6832 (class 0 OID 0)
-- Dependencies: 380
-- Name: stats_track_account_guid_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.stats_track_account_guid_id_seq', 1, false);


--
-- TOC entry 6833 (class 0 OID 0)
-- Dependencies: 398
-- Name: stats_track_event_account_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.stats_track_event_account_id_seq', 1, false);


--
-- TOC entry 6834 (class 0 OID 0)
-- Dependencies: 382
-- Name: stats_track_event_channel_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.stats_track_event_channel_id_seq', 1, false);


--
-- TOC entry 6835 (class 0 OID 0)
-- Dependencies: 390
-- Name: stats_track_event_clip_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.stats_track_event_clip_id_seq', 1, false);


--
-- TOC entry 6836 (class 0 OID 0)
-- Dependencies: 386
-- Name: stats_track_event_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.stats_track_event_item_id_seq', 1, false);


--
-- TOC entry 6837 (class 0 OID 0)
-- Dependencies: 394
-- Name: stats_track_event_playlist_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.stats_track_event_playlist_id_seq', 1, false);


--
-- TOC entry 5813 (class 2606 OID 26051)
-- Name: account_admin_roles account_admin_roles_account_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_admin_roles
    ADD CONSTRAINT account_admin_roles_account_id_key UNIQUE (account_id);


--
-- TOC entry 5815 (class 2606 OID 26049)
-- Name: account_admin_roles account_admin_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_admin_roles
    ADD CONSTRAINT account_admin_roles_pkey PRIMARY KEY (id);


--
-- TOC entry 5915 (class 2606 OID 26391)
-- Name: account_app_store_purchase account_app_store_purchase_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_app_store_purchase
    ADD CONSTRAINT account_app_store_purchase_pkey PRIMARY KEY (transaction_id);


--
-- TOC entry 5776 (class 2606 OID 25931)
-- Name: account_credentials account_credentials_account_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_credentials
    ADD CONSTRAINT account_credentials_account_id_key UNIQUE (account_id);


--
-- TOC entry 5778 (class 2606 OID 25933)
-- Name: account_credentials account_credentials_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_credentials
    ADD CONSTRAINT account_credentials_email_key UNIQUE (email);


--
-- TOC entry 5780 (class 2606 OID 25929)
-- Name: account_credentials account_credentials_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_credentials
    ADD CONSTRAINT account_credentials_pkey PRIMARY KEY (id);


--
-- TOC entry 5798 (class 2606 OID 26001)
-- Name: account_email_change_verification account_email_change_verification_account_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_email_change_verification
    ADD CONSTRAINT account_email_change_verification_account_id_key UNIQUE (account_id);


--
-- TOC entry 5800 (class 2606 OID 25999)
-- Name: account_email_change_verification account_email_change_verification_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_email_change_verification
    ADD CONSTRAINT account_email_change_verification_pkey PRIMARY KEY (id);


--
-- TOC entry 5906 (class 2606 OID 26364)
-- Name: account_fcm_device account_fcm_device_fcm_token_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_fcm_device
    ADD CONSTRAINT account_fcm_device_fcm_token_key UNIQUE (fcm_token);


--
-- TOC entry 5908 (class 2606 OID 26362)
-- Name: account_fcm_device account_fcm_device_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_fcm_device
    ADD CONSTRAINT account_fcm_device_pkey PRIMARY KEY (id);


--
-- TOC entry 5881 (class 2606 OID 26259)
-- Name: account_following_account account_following_account_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_following_account
    ADD CONSTRAINT account_following_account_pkey PRIMARY KEY (account_id, following_account_id);


--
-- TOC entry 5893 (class 2606 OID 26312)
-- Name: account_following_add_by_rss_channel account_following_add_by_rss_channel_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_following_add_by_rss_channel
    ADD CONSTRAINT account_following_add_by_rss_channel_pkey PRIMARY KEY (account_id, feed_url);


--
-- TOC entry 5885 (class 2606 OID 26276)
-- Name: account_following_channel account_following_channel_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_following_channel
    ADD CONSTRAINT account_following_channel_pkey PRIMARY KEY (account_id, channel_id);


--
-- TOC entry 5889 (class 2606 OID 26293)
-- Name: account_following_playlist account_following_playlist_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_following_playlist
    ADD CONSTRAINT account_following_playlist_pkey PRIMARY KEY (account_id, playlist_id);


--
-- TOC entry 5918 (class 2606 OID 26404)
-- Name: account_google_play_purchase account_google_play_purchase_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_google_play_purchase
    ADD CONSTRAINT account_google_play_purchase_pkey PRIMARY KEY (transaction_id);


--
-- TOC entry 5920 (class 2606 OID 26406)
-- Name: account_google_play_purchase account_google_play_purchase_purchase_token_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_google_play_purchase
    ADD CONSTRAINT account_google_play_purchase_purchase_token_key UNIQUE (purchase_token);


--
-- TOC entry 5771 (class 2606 OID 25914)
-- Name: account account_id_text_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_id_text_key UNIQUE (id_text);


--
-- TOC entry 5803 (class 2606 OID 26017)
-- Name: account_membership account_membership_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_membership
    ADD CONSTRAINT account_membership_pkey PRIMARY KEY (id);


--
-- TOC entry 5807 (class 2606 OID 26028)
-- Name: account_membership_status account_membership_status_account_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_membership_status
    ADD CONSTRAINT account_membership_status_account_id_key UNIQUE (account_id);


--
-- TOC entry 5809 (class 2606 OID 26026)
-- Name: account_membership_status account_membership_status_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_membership_status
    ADD CONSTRAINT account_membership_status_pkey PRIMARY KEY (id);


--
-- TOC entry 5805 (class 2606 OID 26019)
-- Name: account_membership account_membership_tier_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_membership
    ADD CONSTRAINT account_membership_tier_key UNIQUE (tier);


--
-- TOC entry 5896 (class 2606 OID 26323)
-- Name: account_notification_channel account_notification_channel_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_notification_channel
    ADD CONSTRAINT account_notification_channel_pkey PRIMARY KEY (channel_id, account_id);


--
-- TOC entry 5912 (class 2606 OID 26378)
-- Name: account_paypal_order account_paypal_order_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_paypal_order
    ADD CONSTRAINT account_paypal_order_pkey PRIMARY KEY (payment_id);


--
-- TOC entry 5773 (class 2606 OID 25912)
-- Name: account account_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_pkey PRIMARY KEY (id);


--
-- TOC entry 5783 (class 2606 OID 25950)
-- Name: account_profile account_profile_account_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_profile
    ADD CONSTRAINT account_profile_account_id_key UNIQUE (account_id);


--
-- TOC entry 5785 (class 2606 OID 25948)
-- Name: account_profile account_profile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_profile
    ADD CONSTRAINT account_profile_pkey PRIMARY KEY (id);


--
-- TOC entry 5788 (class 2606 OID 25967)
-- Name: account_reset_password account_reset_password_account_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_reset_password
    ADD CONSTRAINT account_reset_password_account_id_key UNIQUE (account_id);


--
-- TOC entry 5790 (class 2606 OID 25965)
-- Name: account_reset_password account_reset_password_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_reset_password
    ADD CONSTRAINT account_reset_password_pkey PRIMARY KEY (id);


--
-- TOC entry 5900 (class 2606 OID 26344)
-- Name: account_up_device account_up_device_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_up_device
    ADD CONSTRAINT account_up_device_pkey PRIMARY KEY (id);


--
-- TOC entry 5902 (class 2606 OID 26346)
-- Name: account_up_device account_up_device_up_endpoint_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_up_device
    ADD CONSTRAINT account_up_device_up_endpoint_key UNIQUE (up_endpoint);


--
-- TOC entry 5793 (class 2606 OID 25984)
-- Name: account_verification account_verification_account_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_verification
    ADD CONSTRAINT account_verification_account_id_key UNIQUE (account_id);


--
-- TOC entry 5795 (class 2606 OID 25982)
-- Name: account_verification account_verification_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_verification
    ADD CONSTRAINT account_verification_pkey PRIMARY KEY (id);


--
-- TOC entry 5491 (class 2606 OID 24856)
-- Name: category category_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.category
    ADD CONSTRAINT category_pkey PRIMARY KEY (id);


--
-- TOC entry 5530 (class 2606 OID 24979)
-- Name: channel_about channel_about_channel_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_about
    ADD CONSTRAINT channel_about_channel_id_key UNIQUE (channel_id);


--
-- TOC entry 5532 (class 2606 OID 24977)
-- Name: channel_about channel_about_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_about
    ADD CONSTRAINT channel_about_pkey PRIMARY KEY (id);


--
-- TOC entry 5536 (class 2606 OID 24998)
-- Name: channel_category channel_category_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_category
    ADD CONSTRAINT channel_category_pkey PRIMARY KEY (id);


--
-- TOC entry 5540 (class 2606 OID 25021)
-- Name: channel_chat channel_chat_channel_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_chat
    ADD CONSTRAINT channel_chat_channel_id_key UNIQUE (channel_id);


--
-- TOC entry 5542 (class 2606 OID 25019)
-- Name: channel_chat channel_chat_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_chat
    ADD CONSTRAINT channel_chat_pkey PRIMARY KEY (id);


--
-- TOC entry 5545 (class 2606 OID 25038)
-- Name: channel_description channel_description_channel_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_description
    ADD CONSTRAINT channel_description_channel_id_key UNIQUE (channel_id);


--
-- TOC entry 5547 (class 2606 OID 25036)
-- Name: channel_description channel_description_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_description
    ADD CONSTRAINT channel_description_pkey PRIMARY KEY (id);


--
-- TOC entry 5512 (class 2606 OID 24938)
-- Name: channel channel_feed_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel
    ADD CONSTRAINT channel_feed_id_key UNIQUE (feed_id);


--
-- TOC entry 5550 (class 2606 OID 25053)
-- Name: channel_funding channel_funding_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_funding
    ADD CONSTRAINT channel_funding_pkey PRIMARY KEY (id);


--
-- TOC entry 5514 (class 2606 OID 24936)
-- Name: channel channel_id_text_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel
    ADD CONSTRAINT channel_id_text_key UNIQUE (id_text);


--
-- TOC entry 5553 (class 2606 OID 25069)
-- Name: channel_image channel_image_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_image
    ADD CONSTRAINT channel_image_pkey PRIMARY KEY (id);


--
-- TOC entry 5556 (class 2606 OID 25084)
-- Name: channel_internal_settings channel_internal_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_internal_settings
    ADD CONSTRAINT channel_internal_settings_pkey PRIMARY KEY (id);


--
-- TOC entry 5526 (class 2606 OID 24968)
-- Name: channel_itunes_type channel_itunes_type_itunes_type_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_itunes_type
    ADD CONSTRAINT channel_itunes_type_itunes_type_key UNIQUE (itunes_type);


--
-- TOC entry 5528 (class 2606 OID 24966)
-- Name: channel_itunes_type channel_itunes_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_itunes_type
    ADD CONSTRAINT channel_itunes_type_pkey PRIMARY KEY (id);


--
-- TOC entry 5559 (class 2606 OID 25101)
-- Name: channel_license channel_license_channel_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_license
    ADD CONSTRAINT channel_license_channel_id_key UNIQUE (channel_id);


--
-- TOC entry 5561 (class 2606 OID 25099)
-- Name: channel_license channel_license_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_license
    ADD CONSTRAINT channel_license_pkey PRIMARY KEY (id);


--
-- TOC entry 5564 (class 2606 OID 25119)
-- Name: channel_location channel_location_channel_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_location
    ADD CONSTRAINT channel_location_channel_id_key UNIQUE (channel_id);


--
-- TOC entry 5566 (class 2606 OID 25117)
-- Name: channel_location channel_location_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_location
    ADD CONSTRAINT channel_location_pkey PRIMARY KEY (id);


--
-- TOC entry 5569 (class 2606 OID 25135)
-- Name: channel_person channel_person_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_person
    ADD CONSTRAINT channel_person_pkey PRIMARY KEY (id);


--
-- TOC entry 5516 (class 2606 OID 24934)
-- Name: channel channel_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel
    ADD CONSTRAINT channel_pkey PRIMARY KEY (id);


--
-- TOC entry 5518 (class 2606 OID 24942)
-- Name: channel channel_podcast_guid_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel
    ADD CONSTRAINT channel_podcast_guid_key UNIQUE (podcast_guid);


--
-- TOC entry 5521 (class 2606 OID 24940)
-- Name: channel channel_podcast_index_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel
    ADD CONSTRAINT channel_podcast_index_id_key UNIQUE (podcast_index_id);


--
-- TOC entry 5572 (class 2606 OID 25150)
-- Name: channel_podroll channel_podroll_channel_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_podroll
    ADD CONSTRAINT channel_podroll_channel_id_key UNIQUE (channel_id);


--
-- TOC entry 5574 (class 2606 OID 25148)
-- Name: channel_podroll channel_podroll_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_podroll
    ADD CONSTRAINT channel_podroll_pkey PRIMARY KEY (id);


--
-- TOC entry 5577 (class 2606 OID 25165)
-- Name: channel_podroll_remote_item channel_podroll_remote_item_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_podroll_remote_item
    ADD CONSTRAINT channel_podroll_remote_item_pkey PRIMARY KEY (id);


--
-- TOC entry 5584 (class 2606 OID 25189)
-- Name: channel_publisher channel_publisher_channel_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_publisher
    ADD CONSTRAINT channel_publisher_channel_id_key UNIQUE (channel_id);


--
-- TOC entry 5586 (class 2606 OID 25187)
-- Name: channel_publisher channel_publisher_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_publisher
    ADD CONSTRAINT channel_publisher_pkey PRIMARY KEY (id);


--
-- TOC entry 5589 (class 2606 OID 25206)
-- Name: channel_publisher_remote_item channel_publisher_remote_item_channel_publisher_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_publisher_remote_item
    ADD CONSTRAINT channel_publisher_remote_item_channel_publisher_id_key UNIQUE (channel_publisher_id);


--
-- TOC entry 5591 (class 2606 OID 25204)
-- Name: channel_publisher_remote_item channel_publisher_remote_item_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_publisher_remote_item
    ADD CONSTRAINT channel_publisher_remote_item_pkey PRIMARY KEY (id);


--
-- TOC entry 5598 (class 2606 OID 25230)
-- Name: channel_remote_item channel_remote_item_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_remote_item
    ADD CONSTRAINT channel_remote_item_pkey PRIMARY KEY (id);


--
-- TOC entry 5605 (class 2606 OID 25256)
-- Name: channel_season channel_season_channel_id_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_season
    ADD CONSTRAINT channel_season_channel_id_number_key UNIQUE (channel_id, number);


--
-- TOC entry 5607 (class 2606 OID 25254)
-- Name: channel_season channel_season_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_season
    ADD CONSTRAINT channel_season_pkey PRIMARY KEY (id);


--
-- TOC entry 5610 (class 2606 OID 25271)
-- Name: channel_social_interact channel_social_interact_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_social_interact
    ADD CONSTRAINT channel_social_interact_pkey PRIMARY KEY (id);


--
-- TOC entry 5613 (class 2606 OID 25288)
-- Name: channel_trailer channel_trailer_channel_id_url_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_trailer
    ADD CONSTRAINT channel_trailer_channel_id_url_key UNIQUE (channel_id, url);


--
-- TOC entry 5615 (class 2606 OID 25286)
-- Name: channel_trailer channel_trailer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_trailer
    ADD CONSTRAINT channel_trailer_pkey PRIMARY KEY (id);


--
-- TOC entry 5619 (class 2606 OID 25309)
-- Name: channel_txt channel_txt_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_txt
    ADD CONSTRAINT channel_txt_pkey PRIMARY KEY (id);


--
-- TOC entry 5622 (class 2606 OID 25324)
-- Name: channel_value channel_value_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_value
    ADD CONSTRAINT channel_value_pkey PRIMARY KEY (id);


--
-- TOC entry 5625 (class 2606 OID 25340)
-- Name: channel_value_recipient channel_value_recipient_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_value_recipient
    ADD CONSTRAINT channel_value_recipient_pkey PRIMARY KEY (id);


--
-- TOC entry 5818 (class 2606 OID 26068)
-- Name: clip clip_id_text_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clip
    ADD CONSTRAINT clip_id_text_key UNIQUE (id_text);


--
-- TOC entry 5820 (class 2606 OID 26066)
-- Name: clip clip_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clip
    ADD CONSTRAINT clip_pkey PRIMARY KEY (id);


--
-- TOC entry 5498 (class 2606 OID 24884)
-- Name: feed_flag_status feed_flag_status_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.feed_flag_status
    ADD CONSTRAINT feed_flag_status_pkey PRIMARY KEY (id);


--
-- TOC entry 5500 (class 2606 OID 24886)
-- Name: feed_flag_status feed_flag_status_status_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.feed_flag_status
    ADD CONSTRAINT feed_flag_status_status_key UNIQUE (status);


--
-- TOC entry 5507 (class 2606 OID 24917)
-- Name: feed_log feed_log_feed_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.feed_log
    ADD CONSTRAINT feed_log_feed_id_key UNIQUE (feed_id);


--
-- TOC entry 5509 (class 2606 OID 24915)
-- Name: feed_log feed_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.feed_log
    ADD CONSTRAINT feed_log_pkey PRIMARY KEY (id);


--
-- TOC entry 5502 (class 2606 OID 24898)
-- Name: feed feed_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.feed
    ADD CONSTRAINT feed_pkey PRIMARY KEY (id);


--
-- TOC entry 5504 (class 2606 OID 24900)
-- Name: feed feed_url_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.feed
    ADD CONSTRAINT feed_url_key UNIQUE (url);


--
-- TOC entry 5647 (class 2606 OID 25409)
-- Name: item_about item_about_item_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_about
    ADD CONSTRAINT item_about_item_id_key UNIQUE (item_id);


--
-- TOC entry 5649 (class 2606 OID 25407)
-- Name: item_about item_about_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_about
    ADD CONSTRAINT item_about_pkey PRIMARY KEY (id);


--
-- TOC entry 5662 (class 2606 OID 25466)
-- Name: item_chapter item_chapter_id_text_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_chapter
    ADD CONSTRAINT item_chapter_id_text_key UNIQUE (id_text);


--
-- TOC entry 5667 (class 2606 OID 25484)
-- Name: item_chapter_location item_chapter_location_item_chapter_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_chapter_location
    ADD CONSTRAINT item_chapter_location_item_chapter_id_key UNIQUE (item_chapter_id);


--
-- TOC entry 5669 (class 2606 OID 25482)
-- Name: item_chapter_location item_chapter_location_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_chapter_location
    ADD CONSTRAINT item_chapter_location_pkey PRIMARY KEY (id);


--
-- TOC entry 5664 (class 2606 OID 25464)
-- Name: item_chapter item_chapter_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_chapter
    ADD CONSTRAINT item_chapter_pkey PRIMARY KEY (id);


--
-- TOC entry 5652 (class 2606 OID 25432)
-- Name: item_chapters_feed item_chapters_feed_item_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_chapters_feed
    ADD CONSTRAINT item_chapters_feed_item_id_key UNIQUE (item_id);


--
-- TOC entry 5657 (class 2606 OID 25448)
-- Name: item_chapters_feed_log item_chapters_feed_log_item_chapters_feed_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_chapters_feed_log
    ADD CONSTRAINT item_chapters_feed_log_item_chapters_feed_id_key UNIQUE (item_chapters_feed_id);


--
-- TOC entry 5659 (class 2606 OID 25446)
-- Name: item_chapters_feed_log item_chapters_feed_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_chapters_feed_log
    ADD CONSTRAINT item_chapters_feed_log_pkey PRIMARY KEY (id);


--
-- TOC entry 5654 (class 2606 OID 25430)
-- Name: item_chapters_feed item_chapters_feed_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_chapters_feed
    ADD CONSTRAINT item_chapters_feed_pkey PRIMARY KEY (id);


--
-- TOC entry 5672 (class 2606 OID 25501)
-- Name: item_chat item_chat_item_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_chat
    ADD CONSTRAINT item_chat_item_id_key UNIQUE (item_id);


--
-- TOC entry 5674 (class 2606 OID 25499)
-- Name: item_chat item_chat_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_chat
    ADD CONSTRAINT item_chat_pkey PRIMARY KEY (id);


--
-- TOC entry 5677 (class 2606 OID 25516)
-- Name: item_content_link item_content_link_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_content_link
    ADD CONSTRAINT item_content_link_pkey PRIMARY KEY (id);


--
-- TOC entry 5680 (class 2606 OID 25533)
-- Name: item_description item_description_item_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_description
    ADD CONSTRAINT item_description_item_id_key UNIQUE (item_id);


--
-- TOC entry 5682 (class 2606 OID 25531)
-- Name: item_description item_description_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_description
    ADD CONSTRAINT item_description_pkey PRIMARY KEY (id);


--
-- TOC entry 5691 (class 2606 OID 25582)
-- Name: item_enclosure_integrity item_enclosure_integrity_item_enclosure_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_enclosure_integrity
    ADD CONSTRAINT item_enclosure_integrity_item_enclosure_id_key UNIQUE (item_enclosure_id);


--
-- TOC entry 5693 (class 2606 OID 25580)
-- Name: item_enclosure_integrity item_enclosure_integrity_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_enclosure_integrity
    ADD CONSTRAINT item_enclosure_integrity_pkey PRIMARY KEY (id);


--
-- TOC entry 5685 (class 2606 OID 25549)
-- Name: item_enclosure item_enclosure_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_enclosure
    ADD CONSTRAINT item_enclosure_pkey PRIMARY KEY (id);


--
-- TOC entry 5688 (class 2606 OID 25564)
-- Name: item_enclosure_source item_enclosure_source_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_enclosure_source
    ADD CONSTRAINT item_enclosure_source_pkey PRIMARY KEY (id);


--
-- TOC entry 5628 (class 2606 OID 25356)
-- Name: item_flag_status item_flag_status_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_flag_status
    ADD CONSTRAINT item_flag_status_pkey PRIMARY KEY (id);


--
-- TOC entry 5630 (class 2606 OID 25358)
-- Name: item_flag_status item_flag_status_status_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_flag_status
    ADD CONSTRAINT item_flag_status_status_key UNIQUE (status);


--
-- TOC entry 5696 (class 2606 OID 25597)
-- Name: item_funding item_funding_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_funding
    ADD CONSTRAINT item_funding_pkey PRIMARY KEY (id);


--
-- TOC entry 5636 (class 2606 OID 25371)
-- Name: item item_id_text_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item
    ADD CONSTRAINT item_id_text_key UNIQUE (id_text);


--
-- TOC entry 5699 (class 2606 OID 25613)
-- Name: item_image item_image_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_image
    ADD CONSTRAINT item_image_pkey PRIMARY KEY (id);


--
-- TOC entry 5641 (class 2606 OID 25398)
-- Name: item_itunes_episode_type item_itunes_episode_type_itunes_episode_type_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_itunes_episode_type
    ADD CONSTRAINT item_itunes_episode_type_itunes_episode_type_key UNIQUE (itunes_episode_type);


--
-- TOC entry 5643 (class 2606 OID 25396)
-- Name: item_itunes_episode_type item_itunes_episode_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_itunes_episode_type
    ADD CONSTRAINT item_itunes_episode_type_pkey PRIMARY KEY (id);


--
-- TOC entry 5702 (class 2606 OID 25630)
-- Name: item_license item_license_item_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_license
    ADD CONSTRAINT item_license_item_id_key UNIQUE (item_id);


--
-- TOC entry 5704 (class 2606 OID 25628)
-- Name: item_license item_license_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_license
    ADD CONSTRAINT item_license_pkey PRIMARY KEY (id);


--
-- TOC entry 5707 (class 2606 OID 25648)
-- Name: item_location item_location_item_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_location
    ADD CONSTRAINT item_location_item_id_key UNIQUE (item_id);


--
-- TOC entry 5709 (class 2606 OID 25646)
-- Name: item_location item_location_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_location
    ADD CONSTRAINT item_location_pkey PRIMARY KEY (id);


--
-- TOC entry 5712 (class 2606 OID 25664)
-- Name: item_person item_person_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_person
    ADD CONSTRAINT item_person_pkey PRIMARY KEY (id);


--
-- TOC entry 5638 (class 2606 OID 25369)
-- Name: item item_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item
    ADD CONSTRAINT item_pkey PRIMARY KEY (id);


--
-- TOC entry 5719 (class 2606 OID 25702)
-- Name: item_season_episode item_season_episode_item_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_season_episode
    ADD CONSTRAINT item_season_episode_item_id_key UNIQUE (item_id);


--
-- TOC entry 5721 (class 2606 OID 25700)
-- Name: item_season_episode item_season_episode_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_season_episode
    ADD CONSTRAINT item_season_episode_pkey PRIMARY KEY (id);


--
-- TOC entry 5716 (class 2606 OID 25679)
-- Name: item_season item_season_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_season
    ADD CONSTRAINT item_season_pkey PRIMARY KEY (id);


--
-- TOC entry 5724 (class 2606 OID 25717)
-- Name: item_social_interact item_social_interact_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_social_interact
    ADD CONSTRAINT item_social_interact_pkey PRIMARY KEY (id);


--
-- TOC entry 5727 (class 2606 OID 25734)
-- Name: item_soundbite item_soundbite_id_text_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_soundbite
    ADD CONSTRAINT item_soundbite_id_text_key UNIQUE (id_text);


--
-- TOC entry 5729 (class 2606 OID 25732)
-- Name: item_soundbite item_soundbite_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_soundbite
    ADD CONSTRAINT item_soundbite_pkey PRIMARY KEY (id);


--
-- TOC entry 5732 (class 2606 OID 25750)
-- Name: item_transcript item_transcript_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_transcript
    ADD CONSTRAINT item_transcript_pkey PRIMARY KEY (id);


--
-- TOC entry 5735 (class 2606 OID 25765)
-- Name: item_txt item_txt_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_txt
    ADD CONSTRAINT item_txt_pkey PRIMARY KEY (id);


--
-- TOC entry 5738 (class 2606 OID 25780)
-- Name: item_value item_value_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_value
    ADD CONSTRAINT item_value_pkey PRIMARY KEY (id);


--
-- TOC entry 5741 (class 2606 OID 25796)
-- Name: item_value_recipient item_value_recipient_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_value_recipient
    ADD CONSTRAINT item_value_recipient_pkey PRIMARY KEY (id);


--
-- TOC entry 5744 (class 2606 OID 25813)
-- Name: item_value_time_split item_value_time_split_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_value_time_split
    ADD CONSTRAINT item_value_time_split_pkey PRIMARY KEY (id);


--
-- TOC entry 5755 (class 2606 OID 25849)
-- Name: item_value_time_split_recipient item_value_time_split_recipient_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_value_time_split_recipient
    ADD CONSTRAINT item_value_time_split_recipient_pkey PRIMARY KEY (id);


--
-- TOC entry 5750 (class 2606 OID 25830)
-- Name: item_value_time_split_remote_item item_value_time_split_remote_item_item_value_time_split_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_value_time_split_remote_item
    ADD CONSTRAINT item_value_time_split_remote_item_item_value_time_split_id_key UNIQUE (item_value_time_split_id);


--
-- TOC entry 5752 (class 2606 OID 25828)
-- Name: item_value_time_split_remote_item item_value_time_split_remote_item_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_value_time_split_remote_item
    ADD CONSTRAINT item_value_time_split_remote_item_pkey PRIMARY KEY (id);


--
-- TOC entry 5763 (class 2606 OID 25878)
-- Name: live_item live_item_item_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.live_item
    ADD CONSTRAINT live_item_item_id_key UNIQUE (item_id);


--
-- TOC entry 5765 (class 2606 OID 25876)
-- Name: live_item live_item_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.live_item
    ADD CONSTRAINT live_item_pkey PRIMARY KEY (id);


--
-- TOC entry 5757 (class 2606 OID 25865)
-- Name: live_item_status live_item_status_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.live_item_status
    ADD CONSTRAINT live_item_status_pkey PRIMARY KEY (id);


--
-- TOC entry 5759 (class 2606 OID 25867)
-- Name: live_item_status live_item_status_status_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.live_item_status
    ADD CONSTRAINT live_item_status_status_key UNIQUE (status);


--
-- TOC entry 5494 (class 2606 OID 24872)
-- Name: medium medium_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medium
    ADD CONSTRAINT medium_pkey PRIMARY KEY (id);


--
-- TOC entry 5496 (class 2606 OID 24874)
-- Name: medium medium_value_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medium
    ADD CONSTRAINT medium_value_key UNIQUE (value);


--
-- TOC entry 5924 (class 2606 OID 26420)
-- Name: membership_claim_token membership_claim_token_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.membership_claim_token
    ADD CONSTRAINT membership_claim_token_pkey PRIMARY KEY (id);


--
-- TOC entry 5829 (class 2606 OID 26099)
-- Name: playlist playlist_id_text_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.playlist
    ADD CONSTRAINT playlist_id_text_key UNIQUE (id_text);


--
-- TOC entry 5831 (class 2606 OID 26097)
-- Name: playlist playlist_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.playlist
    ADD CONSTRAINT playlist_pkey PRIMARY KEY (id);


--
-- TOC entry 5839 (class 2606 OID 26128)
-- Name: playlist_resource playlist_resource_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.playlist_resource
    ADD CONSTRAINT playlist_resource_pkey PRIMARY KEY (id);


--
-- TOC entry 5841 (class 2606 OID 26140)
-- Name: playlist_resource playlist_resource_playlist_id_add_by_rss_hash_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.playlist_resource
    ADD CONSTRAINT playlist_resource_playlist_id_add_by_rss_hash_id_key UNIQUE (playlist_id, add_by_rss_hash_id);


--
-- TOC entry 5843 (class 2606 OID 26136)
-- Name: playlist_resource playlist_resource_playlist_id_clip_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.playlist_resource
    ADD CONSTRAINT playlist_resource_playlist_id_clip_id_key UNIQUE (playlist_id, clip_id);


--
-- TOC entry 5845 (class 2606 OID 26134)
-- Name: playlist_resource playlist_resource_playlist_id_item_chapter_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.playlist_resource
    ADD CONSTRAINT playlist_resource_playlist_id_item_chapter_id_key UNIQUE (playlist_id, item_chapter_id);


--
-- TOC entry 5847 (class 2606 OID 26132)
-- Name: playlist_resource playlist_resource_playlist_id_item_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.playlist_resource
    ADD CONSTRAINT playlist_resource_playlist_id_item_id_key UNIQUE (playlist_id, item_id);


--
-- TOC entry 5849 (class 2606 OID 26138)
-- Name: playlist_resource playlist_resource_playlist_id_item_soundbite_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.playlist_resource
    ADD CONSTRAINT playlist_resource_playlist_id_item_soundbite_id_key UNIQUE (playlist_id, item_soundbite_id);


--
-- TOC entry 5851 (class 2606 OID 26130)
-- Name: playlist_resource playlist_resource_playlist_id_list_position_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.playlist_resource
    ADD CONSTRAINT playlist_resource_playlist_id_list_position_key UNIQUE (playlist_id, list_position);


--
-- TOC entry 5855 (class 2606 OID 26186)
-- Name: queue queue_account_id_medium_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.queue
    ADD CONSTRAINT queue_account_id_medium_id_key UNIQUE (account_id, medium_id);


--
-- TOC entry 5857 (class 2606 OID 26184)
-- Name: queue queue_id_text_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.queue
    ADD CONSTRAINT queue_id_text_key UNIQUE (id_text);


--
-- TOC entry 5859 (class 2606 OID 26182)
-- Name: queue queue_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.queue
    ADD CONSTRAINT queue_pkey PRIMARY KEY (id);


--
-- TOC entry 5867 (class 2606 OID 26211)
-- Name: queue_resource queue_resource_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.queue_resource
    ADD CONSTRAINT queue_resource_pkey PRIMARY KEY (id);


--
-- TOC entry 5869 (class 2606 OID 26223)
-- Name: queue_resource queue_resource_queue_id_add_by_rss_hash_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.queue_resource
    ADD CONSTRAINT queue_resource_queue_id_add_by_rss_hash_id_key UNIQUE (queue_id, add_by_rss_hash_id);


--
-- TOC entry 5871 (class 2606 OID 26219)
-- Name: queue_resource queue_resource_queue_id_clip_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.queue_resource
    ADD CONSTRAINT queue_resource_queue_id_clip_id_key UNIQUE (queue_id, clip_id);


--
-- TOC entry 5873 (class 2606 OID 26217)
-- Name: queue_resource queue_resource_queue_id_item_chapter_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.queue_resource
    ADD CONSTRAINT queue_resource_queue_id_item_chapter_id_key UNIQUE (queue_id, item_chapter_id);


--
-- TOC entry 5875 (class 2606 OID 26215)
-- Name: queue_resource queue_resource_queue_id_item_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.queue_resource
    ADD CONSTRAINT queue_resource_queue_id_item_id_key UNIQUE (queue_id, item_id);


--
-- TOC entry 5877 (class 2606 OID 26221)
-- Name: queue_resource queue_resource_queue_id_item_soundbite_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.queue_resource
    ADD CONSTRAINT queue_resource_queue_id_item_soundbite_id_key UNIQUE (queue_id, item_soundbite_id);


--
-- TOC entry 5879 (class 2606 OID 26213)
-- Name: queue_resource queue_resource_queue_id_list_position_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.queue_resource
    ADD CONSTRAINT queue_resource_queue_id_list_position_key UNIQUE (queue_id, list_position);


--
-- TOC entry 5767 (class 2606 OID 25900)
-- Name: sharable_status sharable_status_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sharable_status
    ADD CONSTRAINT sharable_status_pkey PRIMARY KEY (id);


--
-- TOC entry 5769 (class 2606 OID 25902)
-- Name: sharable_status sharable_status_status_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sharable_status
    ADD CONSTRAINT sharable_status_status_key UNIQUE (status);


--
-- TOC entry 6009 (class 2606 OID 26723)
-- Name: stats_aggregated_account stats_aggregated_account_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_aggregated_account
    ADD CONSTRAINT stats_aggregated_account_pkey PRIMARY KEY (id);


--
-- TOC entry 6012 (class 2606 OID 26725)
-- Name: stats_aggregated_account stats_aggregated_account_tracked_account_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_aggregated_account
    ADD CONSTRAINT stats_aggregated_account_tracked_account_id_key UNIQUE (tracked_account_id);


--
-- TOC entry 5944 (class 2606 OID 26493)
-- Name: stats_aggregated_channel stats_aggregated_channel_channel_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_aggregated_channel
    ADD CONSTRAINT stats_aggregated_channel_channel_id_key UNIQUE (channel_id);


--
-- TOC entry 5948 (class 2606 OID 26491)
-- Name: stats_aggregated_channel stats_aggregated_channel_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_aggregated_channel
    ADD CONSTRAINT stats_aggregated_channel_pkey PRIMARY KEY (id);


--
-- TOC entry 5976 (class 2606 OID 26609)
-- Name: stats_aggregated_clip stats_aggregated_clip_clip_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_aggregated_clip
    ADD CONSTRAINT stats_aggregated_clip_clip_id_key UNIQUE (clip_id);


--
-- TOC entry 5980 (class 2606 OID 26607)
-- Name: stats_aggregated_clip stats_aggregated_clip_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_aggregated_clip
    ADD CONSTRAINT stats_aggregated_clip_pkey PRIMARY KEY (id);


--
-- TOC entry 5961 (class 2606 OID 26551)
-- Name: stats_aggregated_item stats_aggregated_item_item_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_aggregated_item
    ADD CONSTRAINT stats_aggregated_item_item_id_key UNIQUE (item_id);


--
-- TOC entry 5964 (class 2606 OID 26549)
-- Name: stats_aggregated_item stats_aggregated_item_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_aggregated_item
    ADD CONSTRAINT stats_aggregated_item_pkey PRIMARY KEY (id);


--
-- TOC entry 5993 (class 2606 OID 26665)
-- Name: stats_aggregated_playlist stats_aggregated_playlist_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_aggregated_playlist
    ADD CONSTRAINT stats_aggregated_playlist_pkey PRIMARY KEY (id);


--
-- TOC entry 5996 (class 2606 OID 26667)
-- Name: stats_aggregated_playlist stats_aggregated_playlist_playlist_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_aggregated_playlist
    ADD CONSTRAINT stats_aggregated_playlist_playlist_id_key UNIQUE (playlist_id);


--
-- TOC entry 5927 (class 2606 OID 26437)
-- Name: stats_track_account_guid stats_track_account_guid_account_guid_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_account_guid
    ADD CONSTRAINT stats_track_account_guid_account_guid_key UNIQUE (account_guid);


--
-- TOC entry 5930 (class 2606 OID 26435)
-- Name: stats_track_account_guid stats_track_account_guid_account_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_account_guid
    ADD CONSTRAINT stats_track_account_guid_account_id_key UNIQUE (account_id);


--
-- TOC entry 5932 (class 2606 OID 26433)
-- Name: stats_track_account_guid stats_track_account_guid_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_account_guid
    ADD CONSTRAINT stats_track_account_guid_pkey PRIMARY KEY (id);


--
-- TOC entry 6000 (class 2606 OID 26686)
-- Name: stats_track_event_account stats_track_event_account_account_guid_tracked_account_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_event_account
    ADD CONSTRAINT stats_track_event_account_account_guid_tracked_account_id_key UNIQUE (account_guid, tracked_account_id);


--
-- TOC entry 6003 (class 2606 OID 26684)
-- Name: stats_track_event_account stats_track_event_account_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_event_account
    ADD CONSTRAINT stats_track_event_account_pkey PRIMARY KEY (id);


--
-- TOC entry 5935 (class 2606 OID 26454)
-- Name: stats_track_event_channel stats_track_event_channel_account_guid_channel_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_event_channel
    ADD CONSTRAINT stats_track_event_channel_account_guid_channel_id_key UNIQUE (account_guid, channel_id);


--
-- TOC entry 5940 (class 2606 OID 26452)
-- Name: stats_track_event_channel stats_track_event_channel_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_event_channel
    ADD CONSTRAINT stats_track_event_channel_pkey PRIMARY KEY (id);


--
-- TOC entry 5967 (class 2606 OID 26570)
-- Name: stats_track_event_clip stats_track_event_clip_account_guid_clip_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_event_clip
    ADD CONSTRAINT stats_track_event_clip_account_guid_clip_id_key UNIQUE (account_guid, clip_id);


--
-- TOC entry 5972 (class 2606 OID 26568)
-- Name: stats_track_event_clip stats_track_event_clip_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_event_clip
    ADD CONSTRAINT stats_track_event_clip_pkey PRIMARY KEY (id);


--
-- TOC entry 5952 (class 2606 OID 26512)
-- Name: stats_track_event_item stats_track_event_item_account_guid_item_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_event_item
    ADD CONSTRAINT stats_track_event_item_account_guid_item_id_key UNIQUE (account_guid, item_id);


--
-- TOC entry 5956 (class 2606 OID 26510)
-- Name: stats_track_event_item stats_track_event_item_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_event_item
    ADD CONSTRAINT stats_track_event_item_pkey PRIMARY KEY (id);


--
-- TOC entry 5984 (class 2606 OID 26628)
-- Name: stats_track_event_playlist stats_track_event_playlist_account_guid_playlist_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_event_playlist
    ADD CONSTRAINT stats_track_event_playlist_account_guid_playlist_id_key UNIQUE (account_guid, playlist_id);


--
-- TOC entry 5987 (class 2606 OID 26626)
-- Name: stats_track_event_playlist stats_track_event_playlist_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_event_playlist
    ADD CONSTRAINT stats_track_event_playlist_pkey PRIMARY KEY (id);


--
-- TOC entry 5519 (class 1259 OID 24953)
-- Name: channel_podcast_guid_unique; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX channel_podcast_guid_unique ON public.channel USING btree (podcast_guid) WHERE (podcast_guid IS NOT NULL);


--
-- TOC entry 5522 (class 1259 OID 24954)
-- Name: channel_slug; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX channel_slug ON public.channel USING btree (slug) WHERE (slug IS NOT NULL);


--
-- TOC entry 5816 (class 1259 OID 26057)
-- Name: idx_account_admin_roles_account_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_account_admin_roles_account_id ON public.account_admin_roles USING btree (account_id);


--
-- TOC entry 5916 (class 1259 OID 26397)
-- Name: idx_account_app_store_purchase_account_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_account_app_store_purchase_account_id ON public.account_app_store_purchase USING btree (account_id);


--
-- TOC entry 5781 (class 1259 OID 25939)
-- Name: idx_account_credentials_account_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_account_credentials_account_id ON public.account_credentials USING btree (account_id);


--
-- TOC entry 5801 (class 1259 OID 26007)
-- Name: idx_account_email_change_verification_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_account_email_change_verification_id ON public.account_email_change_verification USING btree (account_id);


--
-- TOC entry 5909 (class 1259 OID 26370)
-- Name: idx_account_fcm_device_account_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_account_fcm_device_account_id ON public.account_fcm_device USING btree (account_id);


--
-- TOC entry 5910 (class 1259 OID 26371)
-- Name: idx_account_fcm_device_fcm_token; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_account_fcm_device_fcm_token ON public.account_fcm_device USING btree (fcm_token);


--
-- TOC entry 5882 (class 1259 OID 26270)
-- Name: idx_account_following_account_account_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_account_following_account_account_id ON public.account_following_account USING btree (account_id);


--
-- TOC entry 5883 (class 1259 OID 26271)
-- Name: idx_account_following_account_following_account_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_account_following_account_following_account_id ON public.account_following_account USING btree (following_account_id);


--
-- TOC entry 5894 (class 1259 OID 26318)
-- Name: idx_account_following_add_by_rss_channel_account_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_account_following_add_by_rss_channel_account_id ON public.account_following_add_by_rss_channel USING btree (account_id);


--
-- TOC entry 5886 (class 1259 OID 26287)
-- Name: idx_account_following_channel_account_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_account_following_channel_account_id ON public.account_following_channel USING btree (account_id);


--
-- TOC entry 5887 (class 1259 OID 26288)
-- Name: idx_account_following_channel_channel_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_account_following_channel_channel_id ON public.account_following_channel USING btree (channel_id);


--
-- TOC entry 5890 (class 1259 OID 26304)
-- Name: idx_account_following_playlist_account_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_account_following_playlist_account_id ON public.account_following_playlist USING btree (account_id);


--
-- TOC entry 5891 (class 1259 OID 26305)
-- Name: idx_account_following_playlist_playlist_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_account_following_playlist_playlist_id ON public.account_following_playlist USING btree (playlist_id);


--
-- TOC entry 5921 (class 1259 OID 26412)
-- Name: idx_account_google_play_purchase_account_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_account_google_play_purchase_account_id ON public.account_google_play_purchase USING btree (account_id);


--
-- TOC entry 5810 (class 1259 OID 26039)
-- Name: idx_account_membership_status_account_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_account_membership_status_account_id ON public.account_membership_status USING btree (account_id);


--
-- TOC entry 5811 (class 1259 OID 26040)
-- Name: idx_account_membership_status_account_membership_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_account_membership_status_account_membership_id ON public.account_membership_status USING btree (account_membership_id);


--
-- TOC entry 5897 (class 1259 OID 26335)
-- Name: idx_account_notification_channel_account_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_account_notification_channel_account_id ON public.account_notification_channel USING btree (account_id);


--
-- TOC entry 5898 (class 1259 OID 26334)
-- Name: idx_account_notification_channel_channel_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_account_notification_channel_channel_id ON public.account_notification_channel USING btree (channel_id);


--
-- TOC entry 5913 (class 1259 OID 26384)
-- Name: idx_account_paypal_order_account_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_account_paypal_order_account_id ON public.account_paypal_order USING btree (account_id);


--
-- TOC entry 5786 (class 1259 OID 25956)
-- Name: idx_account_profile_account_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_account_profile_account_id ON public.account_profile USING btree (account_id);


--
-- TOC entry 5791 (class 1259 OID 25973)
-- Name: idx_account_reset_password_account_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_account_reset_password_account_id ON public.account_reset_password USING btree (account_id);


--
-- TOC entry 5774 (class 1259 OID 25920)
-- Name: idx_account_sharable_status_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_account_sharable_status_id ON public.account USING btree (sharable_status_id);


--
-- TOC entry 5903 (class 1259 OID 26352)
-- Name: idx_account_up_device_account_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_account_up_device_account_id ON public.account_up_device USING btree (account_id);


--
-- TOC entry 5904 (class 1259 OID 26353)
-- Name: idx_account_up_device_up_endpoint; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_account_up_device_up_endpoint ON public.account_up_device USING btree (up_endpoint);


--
-- TOC entry 5796 (class 1259 OID 25990)
-- Name: idx_account_verification_account_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_account_verification_account_id ON public.account_verification USING btree (account_id);


--
-- TOC entry 5492 (class 1259 OID 24862)
-- Name: idx_category_parent_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_category_parent_id ON public.category USING btree (parent_id);


--
-- TOC entry 5533 (class 1259 OID 24990)
-- Name: idx_channel_about_channel_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_about_channel_id ON public.channel_about USING btree (channel_id);


--
-- TOC entry 5534 (class 1259 OID 24991)
-- Name: idx_channel_about_itunes_type_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_about_itunes_type_id ON public.channel_about USING btree (itunes_type_id);


--
-- TOC entry 5537 (class 1259 OID 25010)
-- Name: idx_channel_category_category_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_category_category_id ON public.channel_category USING btree (category_id);


--
-- TOC entry 5538 (class 1259 OID 25009)
-- Name: idx_channel_category_channel_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_category_channel_id ON public.channel_category USING btree (channel_id);


--
-- TOC entry 5543 (class 1259 OID 25027)
-- Name: idx_channel_chat_channel_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_chat_channel_id ON public.channel_chat USING btree (channel_id);


--
-- TOC entry 5548 (class 1259 OID 25044)
-- Name: idx_channel_description_channel_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_description_channel_id ON public.channel_description USING btree (channel_id);


--
-- TOC entry 5523 (class 1259 OID 24955)
-- Name: idx_channel_feed_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_feed_id ON public.channel USING btree (feed_id);


--
-- TOC entry 5551 (class 1259 OID 25059)
-- Name: idx_channel_funding_channel_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_funding_channel_id ON public.channel_funding USING btree (channel_id);


--
-- TOC entry 5554 (class 1259 OID 25075)
-- Name: idx_channel_image_channel_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_image_channel_id ON public.channel_image USING btree (channel_id);


--
-- TOC entry 5557 (class 1259 OID 25090)
-- Name: idx_channel_internal_settings_channel_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_internal_settings_channel_id ON public.channel_internal_settings USING btree (channel_id);


--
-- TOC entry 5562 (class 1259 OID 25107)
-- Name: idx_channel_license_channel_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_license_channel_id ON public.channel_license USING btree (channel_id);


--
-- TOC entry 5567 (class 1259 OID 25125)
-- Name: idx_channel_location_channel_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_location_channel_id ON public.channel_location USING btree (channel_id);


--
-- TOC entry 5524 (class 1259 OID 24956)
-- Name: idx_channel_medium_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_medium_id ON public.channel USING btree (medium_id);


--
-- TOC entry 5570 (class 1259 OID 25141)
-- Name: idx_channel_person_channel_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_person_channel_id ON public.channel_person USING btree (channel_id);


--
-- TOC entry 5575 (class 1259 OID 25156)
-- Name: idx_channel_podroll_channel_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_podroll_channel_id ON public.channel_podroll USING btree (channel_id);


--
-- TOC entry 5578 (class 1259 OID 25176)
-- Name: idx_channel_podroll_remote_item_channel_podroll_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_podroll_remote_item_channel_podroll_id ON public.channel_podroll_remote_item USING btree (channel_podroll_id);


--
-- TOC entry 5579 (class 1259 OID 25178)
-- Name: idx_channel_podroll_remote_item_feed_guid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_podroll_remote_item_feed_guid ON public.channel_podroll_remote_item USING btree (feed_guid);


--
-- TOC entry 5580 (class 1259 OID 25179)
-- Name: idx_channel_podroll_remote_item_feed_url; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_podroll_remote_item_feed_url ON public.channel_podroll_remote_item USING btree (feed_url);


--
-- TOC entry 5581 (class 1259 OID 25180)
-- Name: idx_channel_podroll_remote_item_item_guid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_podroll_remote_item_item_guid ON public.channel_podroll_remote_item USING btree (item_guid);


--
-- TOC entry 5582 (class 1259 OID 25177)
-- Name: idx_channel_podroll_remote_item_medium_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_podroll_remote_item_medium_id ON public.channel_podroll_remote_item USING btree (medium_id);


--
-- TOC entry 5587 (class 1259 OID 25195)
-- Name: idx_channel_publisher_channel_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_publisher_channel_id ON public.channel_publisher USING btree (channel_id);


--
-- TOC entry 5592 (class 1259 OID 25217)
-- Name: idx_channel_publisher_remote_item_channel_publisher_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_publisher_remote_item_channel_publisher_id ON public.channel_publisher_remote_item USING btree (channel_publisher_id);


--
-- TOC entry 5593 (class 1259 OID 25219)
-- Name: idx_channel_publisher_remote_item_feed_guid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_publisher_remote_item_feed_guid ON public.channel_publisher_remote_item USING btree (feed_guid);


--
-- TOC entry 5594 (class 1259 OID 25220)
-- Name: idx_channel_publisher_remote_item_feed_url; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_publisher_remote_item_feed_url ON public.channel_publisher_remote_item USING btree (feed_url);


--
-- TOC entry 5595 (class 1259 OID 25221)
-- Name: idx_channel_publisher_remote_item_item_guid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_publisher_remote_item_item_guid ON public.channel_publisher_remote_item USING btree (item_guid);


--
-- TOC entry 5596 (class 1259 OID 25218)
-- Name: idx_channel_publisher_remote_item_medium_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_publisher_remote_item_medium_id ON public.channel_publisher_remote_item USING btree (medium_id);


--
-- TOC entry 5599 (class 1259 OID 25241)
-- Name: idx_channel_remote_item_channel_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_remote_item_channel_id ON public.channel_remote_item USING btree (channel_id);


--
-- TOC entry 5600 (class 1259 OID 25243)
-- Name: idx_channel_remote_item_feed_guid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_remote_item_feed_guid ON public.channel_remote_item USING btree (feed_guid);


--
-- TOC entry 5601 (class 1259 OID 25244)
-- Name: idx_channel_remote_item_feed_url; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_remote_item_feed_url ON public.channel_remote_item USING btree (feed_url);


--
-- TOC entry 5602 (class 1259 OID 25245)
-- Name: idx_channel_remote_item_item_guid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_remote_item_item_guid ON public.channel_remote_item USING btree (item_guid);


--
-- TOC entry 5603 (class 1259 OID 25242)
-- Name: idx_channel_remote_item_medium_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_remote_item_medium_id ON public.channel_remote_item USING btree (medium_id);


--
-- TOC entry 5608 (class 1259 OID 25262)
-- Name: idx_channel_season_channel_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_season_channel_id ON public.channel_season USING btree (channel_id);


--
-- TOC entry 5611 (class 1259 OID 25277)
-- Name: idx_channel_social_interact_channel_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_social_interact_channel_id ON public.channel_social_interact USING btree (channel_id);


--
-- TOC entry 5616 (class 1259 OID 25299)
-- Name: idx_channel_trailer_channel_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_trailer_channel_id ON public.channel_trailer USING btree (channel_id);


--
-- TOC entry 5617 (class 1259 OID 25300)
-- Name: idx_channel_trailer_channel_season_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_trailer_channel_season_id ON public.channel_trailer USING btree (channel_season_id);


--
-- TOC entry 5620 (class 1259 OID 25315)
-- Name: idx_channel_txt_channel_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_txt_channel_id ON public.channel_txt USING btree (channel_id);


--
-- TOC entry 5623 (class 1259 OID 25330)
-- Name: idx_channel_value_channel_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_value_channel_id ON public.channel_value USING btree (channel_id);


--
-- TOC entry 5626 (class 1259 OID 25346)
-- Name: idx_channel_value_recipient_channel_value_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_channel_value_recipient_channel_value_id ON public.channel_value_recipient USING btree (channel_value_id);


--
-- TOC entry 5821 (class 1259 OID 26084)
-- Name: idx_clip_account_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_clip_account_id ON public.clip USING btree (account_id);


--
-- TOC entry 5822 (class 1259 OID 26085)
-- Name: idx_clip_item_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_clip_item_id ON public.clip USING btree (item_id);


--
-- TOC entry 5823 (class 1259 OID 26086)
-- Name: idx_clip_sharable_status_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_clip_sharable_status_id ON public.clip USING btree (sharable_status_id);


--
-- TOC entry 5505 (class 1259 OID 24906)
-- Name: idx_feed_feed_flag_status_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_feed_feed_flag_status_id ON public.feed USING btree (feed_flag_status_id);


--
-- TOC entry 5510 (class 1259 OID 24923)
-- Name: idx_feed_log_feed_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_feed_log_feed_id ON public.feed_log USING btree (feed_id);


--
-- TOC entry 5644 (class 1259 OID 25420)
-- Name: idx_item_about_item_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_about_item_id ON public.item_about USING btree (item_id);


--
-- TOC entry 5645 (class 1259 OID 25421)
-- Name: idx_item_about_item_itunes_episode_type_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_about_item_itunes_episode_type_id ON public.item_about USING btree (item_itunes_episode_type_id);


--
-- TOC entry 5631 (class 1259 OID 25383)
-- Name: idx_item_channel_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_channel_id ON public.item USING btree (channel_id);


--
-- TOC entry 5660 (class 1259 OID 25472)
-- Name: idx_item_chapter_item_chapters_feed_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_chapter_item_chapters_feed_id ON public.item_chapter USING btree (item_chapters_feed_id);


--
-- TOC entry 5665 (class 1259 OID 25490)
-- Name: idx_item_chapter_location_item_chapter_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_chapter_location_item_chapter_id ON public.item_chapter_location USING btree (item_chapter_id);


--
-- TOC entry 5650 (class 1259 OID 25438)
-- Name: idx_item_chapters_feed_item_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_chapters_feed_item_id ON public.item_chapters_feed USING btree (item_id);


--
-- TOC entry 5655 (class 1259 OID 25454)
-- Name: idx_item_chapters_feed_log_item_chapters_feed_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_chapters_feed_log_item_chapters_feed_id ON public.item_chapters_feed_log USING btree (item_chapters_feed_id);


--
-- TOC entry 5670 (class 1259 OID 25507)
-- Name: idx_item_chat_item_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_chat_item_id ON public.item_chat USING btree (item_id);


--
-- TOC entry 5675 (class 1259 OID 25522)
-- Name: idx_item_content_link_item_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_content_link_item_id ON public.item_content_link USING btree (item_id);


--
-- TOC entry 5678 (class 1259 OID 25539)
-- Name: idx_item_description_item_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_description_item_id ON public.item_description USING btree (item_id);


--
-- TOC entry 5689 (class 1259 OID 25588)
-- Name: idx_item_enclosure_integrity_item_enclosure_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_enclosure_integrity_item_enclosure_id ON public.item_enclosure_integrity USING btree (item_enclosure_id);


--
-- TOC entry 5683 (class 1259 OID 25555)
-- Name: idx_item_enclosure_item_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_enclosure_item_id ON public.item_enclosure USING btree (item_id);


--
-- TOC entry 5686 (class 1259 OID 25570)
-- Name: idx_item_enclosure_source_item_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_enclosure_source_item_id ON public.item_enclosure_source USING btree (item_enclosure_id);


--
-- TOC entry 5694 (class 1259 OID 25603)
-- Name: idx_item_funding_item_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_funding_item_id ON public.item_funding USING btree (item_id);


--
-- TOC entry 5632 (class 1259 OID 25384)
-- Name: idx_item_guid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_guid ON public.item USING btree (guid);


--
-- TOC entry 5633 (class 1259 OID 25385)
-- Name: idx_item_guid_enclosure_url; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_guid_enclosure_url ON public.item USING btree (guid_enclosure_url);


--
-- TOC entry 5697 (class 1259 OID 25619)
-- Name: idx_item_image_item_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_image_item_id ON public.item_image USING btree (item_id);


--
-- TOC entry 5634 (class 1259 OID 25386)
-- Name: idx_item_item_flag_status_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_item_flag_status_id ON public.item USING btree (item_flag_status_id);


--
-- TOC entry 5700 (class 1259 OID 25636)
-- Name: idx_item_license_item_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_license_item_id ON public.item_license USING btree (item_id);


--
-- TOC entry 5705 (class 1259 OID 25654)
-- Name: idx_item_location_item_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_location_item_id ON public.item_location USING btree (item_id);


--
-- TOC entry 5710 (class 1259 OID 25670)
-- Name: idx_item_person_item_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_person_item_id ON public.item_person USING btree (item_id);


--
-- TOC entry 5713 (class 1259 OID 25690)
-- Name: idx_item_season_channel_season_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_season_channel_season_id ON public.item_season USING btree (channel_season_id);


--
-- TOC entry 5717 (class 1259 OID 25708)
-- Name: idx_item_season_episode_item_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_season_episode_item_id ON public.item_season_episode USING btree (item_id);


--
-- TOC entry 5714 (class 1259 OID 25691)
-- Name: idx_item_season_item_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_season_item_id ON public.item_season USING btree (item_id);


--
-- TOC entry 5722 (class 1259 OID 25723)
-- Name: idx_item_social_interact_item_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_social_interact_item_id ON public.item_social_interact USING btree (item_id);


--
-- TOC entry 5725 (class 1259 OID 25740)
-- Name: idx_item_soundbite_item_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_soundbite_item_id ON public.item_soundbite USING btree (item_id);


--
-- TOC entry 5730 (class 1259 OID 25756)
-- Name: idx_item_transcript_item_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_transcript_item_id ON public.item_transcript USING btree (item_id);


--
-- TOC entry 5733 (class 1259 OID 25771)
-- Name: idx_item_txt_item_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_txt_item_id ON public.item_txt USING btree (item_id);


--
-- TOC entry 5736 (class 1259 OID 25786)
-- Name: idx_item_value_item_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_value_item_id ON public.item_value USING btree (item_id);


--
-- TOC entry 5739 (class 1259 OID 25802)
-- Name: idx_item_value_recipient_item_value_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_value_recipient_item_value_id ON public.item_value_recipient USING btree (item_value_id);


--
-- TOC entry 5742 (class 1259 OID 25819)
-- Name: idx_item_value_time_split_item_value_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_value_time_split_item_value_id ON public.item_value_time_split USING btree (item_value_id);


--
-- TOC entry 5753 (class 1259 OID 25855)
-- Name: idx_item_value_time_split_recipient_item_value_time_split_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_value_time_split_recipient_item_value_time_split_id ON public.item_value_time_split_recipient USING btree (item_value_time_split_id);


--
-- TOC entry 5745 (class 1259 OID 25837)
-- Name: idx_item_value_time_split_remote_item_feed_guid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_value_time_split_remote_item_feed_guid ON public.item_value_time_split_remote_item USING btree (feed_guid);


--
-- TOC entry 5746 (class 1259 OID 25838)
-- Name: idx_item_value_time_split_remote_item_feed_url; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_value_time_split_remote_item_feed_url ON public.item_value_time_split_remote_item USING btree (feed_url);


--
-- TOC entry 5747 (class 1259 OID 25839)
-- Name: idx_item_value_time_split_remote_item_item_guid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_value_time_split_remote_item_item_guid ON public.item_value_time_split_remote_item USING btree (item_guid);


--
-- TOC entry 5748 (class 1259 OID 25836)
-- Name: idx_item_value_time_split_remote_item_item_value_time_split_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_item_value_time_split_remote_item_item_value_time_split_id ON public.item_value_time_split_remote_item USING btree (item_value_time_split_id);


--
-- TOC entry 5760 (class 1259 OID 25889)
-- Name: idx_live_item_item_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_live_item_item_id ON public.live_item USING btree (item_id);


--
-- TOC entry 5761 (class 1259 OID 25890)
-- Name: idx_live_item_live_item_status_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_live_item_live_item_status_id ON public.live_item USING btree (live_item_status_id);


--
-- TOC entry 5922 (class 1259 OID 26426)
-- Name: idx_membership_claim_token_account_membership_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_membership_claim_token_account_membership_id ON public.membership_claim_token USING btree (account_membership_id);


--
-- TOC entry 5824 (class 1259 OID 26116)
-- Name: idx_playlist_account_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_playlist_account_id ON public.playlist USING btree (account_id);


--
-- TOC entry 5825 (class 1259 OID 26115)
-- Name: idx_playlist_account_medium_default_favorites; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX idx_playlist_account_medium_default_favorites ON public.playlist USING btree (account_id, medium_id) WHERE (is_default_favorites = true);


--
-- TOC entry 5826 (class 1259 OID 26118)
-- Name: idx_playlist_medium_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_playlist_medium_id ON public.playlist USING btree (medium_id);


--
-- TOC entry 5832 (class 1259 OID 26169)
-- Name: idx_playlist_resource_clip_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_playlist_resource_clip_id ON public.playlist_resource USING btree (clip_id);


--
-- TOC entry 5833 (class 1259 OID 26171)
-- Name: idx_playlist_resource_hash_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_playlist_resource_hash_id ON public.playlist_resource USING btree (add_by_rss_hash_id);


--
-- TOC entry 5834 (class 1259 OID 26168)
-- Name: idx_playlist_resource_item_chapter_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_playlist_resource_item_chapter_id ON public.playlist_resource USING btree (item_chapter_id);


--
-- TOC entry 5835 (class 1259 OID 26167)
-- Name: idx_playlist_resource_item_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_playlist_resource_item_id ON public.playlist_resource USING btree (item_id);


--
-- TOC entry 5836 (class 1259 OID 26166)
-- Name: idx_playlist_resource_playlist_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_playlist_resource_playlist_id ON public.playlist_resource USING btree (playlist_id);


--
-- TOC entry 5837 (class 1259 OID 26170)
-- Name: idx_playlist_resource_soundbite_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_playlist_resource_soundbite_id ON public.playlist_resource USING btree (item_soundbite_id);


--
-- TOC entry 5827 (class 1259 OID 26117)
-- Name: idx_playlist_sharable_status_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_playlist_sharable_status_id ON public.playlist USING btree (sharable_status_id);


--
-- TOC entry 5852 (class 1259 OID 26197)
-- Name: idx_queue_account_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_queue_account_id ON public.queue USING btree (account_id);


--
-- TOC entry 5853 (class 1259 OID 26198)
-- Name: idx_queue_medium_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_queue_medium_id ON public.queue USING btree (medium_id);


--
-- TOC entry 5860 (class 1259 OID 26254)
-- Name: idx_queue_resource_add_by_rss_hash_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_queue_resource_add_by_rss_hash_id ON public.queue_resource USING btree (add_by_rss_hash_id);


--
-- TOC entry 5861 (class 1259 OID 26252)
-- Name: idx_queue_resource_clip_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_queue_resource_clip_id ON public.queue_resource USING btree (clip_id);


--
-- TOC entry 5862 (class 1259 OID 26251)
-- Name: idx_queue_resource_item_chapter_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_queue_resource_item_chapter_id ON public.queue_resource USING btree (item_chapter_id);


--
-- TOC entry 5863 (class 1259 OID 26250)
-- Name: idx_queue_resource_item_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_queue_resource_item_id ON public.queue_resource USING btree (item_id);


--
-- TOC entry 5864 (class 1259 OID 26249)
-- Name: idx_queue_resource_queue_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_queue_resource_queue_id ON public.queue_resource USING btree (queue_id);


--
-- TOC entry 5865 (class 1259 OID 26253)
-- Name: idx_queue_resource_soundbite_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_queue_resource_soundbite_id ON public.queue_resource USING btree (item_soundbite_id);


--
-- TOC entry 5639 (class 1259 OID 25382)
-- Name: item_slug; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX item_slug ON public.item USING btree (slug) WHERE (slug IS NOT NULL);


--
-- TOC entry 6005 (class 1259 OID 26735)
-- Name: stats_aggregated_account_all_time_count_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_aggregated_account_all_time_count_idx ON public.stats_aggregated_account USING btree (all_time_count);


--
-- TOC entry 6006 (class 1259 OID 26732)
-- Name: stats_aggregated_account_day_current_count_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_aggregated_account_day_current_count_idx ON public.stats_aggregated_account USING btree (day_current_count);


--
-- TOC entry 6007 (class 1259 OID 26734)
-- Name: stats_aggregated_account_month_current_count_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_aggregated_account_month_current_count_idx ON public.stats_aggregated_account USING btree (month_current_count);


--
-- TOC entry 6010 (class 1259 OID 26731)
-- Name: stats_aggregated_account_tracked_account_id_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_aggregated_account_tracked_account_id_idx ON public.stats_aggregated_account USING btree (tracked_account_id);


--
-- TOC entry 6013 (class 1259 OID 26733)
-- Name: stats_aggregated_account_week_current_count_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_aggregated_account_week_current_count_idx ON public.stats_aggregated_account USING btree (week_current_count);


--
-- TOC entry 5941 (class 1259 OID 26503)
-- Name: stats_aggregated_channel_all_time_count_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_aggregated_channel_all_time_count_idx ON public.stats_aggregated_channel USING btree (all_time_count);


--
-- TOC entry 5942 (class 1259 OID 26499)
-- Name: stats_aggregated_channel_channel_id_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_aggregated_channel_channel_id_idx ON public.stats_aggregated_channel USING btree (channel_id);


--
-- TOC entry 5945 (class 1259 OID 26500)
-- Name: stats_aggregated_channel_day_current_count_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_aggregated_channel_day_current_count_idx ON public.stats_aggregated_channel USING btree (day_current_count);


--
-- TOC entry 5946 (class 1259 OID 26502)
-- Name: stats_aggregated_channel_month_current_count_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_aggregated_channel_month_current_count_idx ON public.stats_aggregated_channel USING btree (month_current_count);


--
-- TOC entry 5949 (class 1259 OID 26501)
-- Name: stats_aggregated_channel_week_current_count_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_aggregated_channel_week_current_count_idx ON public.stats_aggregated_channel USING btree (week_current_count);


--
-- TOC entry 5973 (class 1259 OID 26619)
-- Name: stats_aggregated_clip_all_time_count_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_aggregated_clip_all_time_count_idx ON public.stats_aggregated_clip USING btree (all_time_count);


--
-- TOC entry 5974 (class 1259 OID 26615)
-- Name: stats_aggregated_clip_clip_id_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_aggregated_clip_clip_id_idx ON public.stats_aggregated_clip USING btree (clip_id);


--
-- TOC entry 5977 (class 1259 OID 26616)
-- Name: stats_aggregated_clip_day_current_count_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_aggregated_clip_day_current_count_idx ON public.stats_aggregated_clip USING btree (day_current_count);


--
-- TOC entry 5978 (class 1259 OID 26618)
-- Name: stats_aggregated_clip_month_current_count_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_aggregated_clip_month_current_count_idx ON public.stats_aggregated_clip USING btree (month_current_count);


--
-- TOC entry 5981 (class 1259 OID 26617)
-- Name: stats_aggregated_clip_week_current_count_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_aggregated_clip_week_current_count_idx ON public.stats_aggregated_clip USING btree (week_current_count);


--
-- TOC entry 5957 (class 1259 OID 26561)
-- Name: stats_aggregated_item_all_time_count_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_aggregated_item_all_time_count_idx ON public.stats_aggregated_item USING btree (all_time_count);


--
-- TOC entry 5958 (class 1259 OID 26558)
-- Name: stats_aggregated_item_day_current_count_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_aggregated_item_day_current_count_idx ON public.stats_aggregated_item USING btree (day_current_count);


--
-- TOC entry 5959 (class 1259 OID 26557)
-- Name: stats_aggregated_item_item_id_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_aggregated_item_item_id_idx ON public.stats_aggregated_item USING btree (item_id);


--
-- TOC entry 5962 (class 1259 OID 26560)
-- Name: stats_aggregated_item_month_current_count_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_aggregated_item_month_current_count_idx ON public.stats_aggregated_item USING btree (month_current_count);


--
-- TOC entry 5965 (class 1259 OID 26559)
-- Name: stats_aggregated_item_week_current_count_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_aggregated_item_week_current_count_idx ON public.stats_aggregated_item USING btree (week_current_count);


--
-- TOC entry 5989 (class 1259 OID 26677)
-- Name: stats_aggregated_playlist_all_time_count_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_aggregated_playlist_all_time_count_idx ON public.stats_aggregated_playlist USING btree (all_time_count);


--
-- TOC entry 5990 (class 1259 OID 26674)
-- Name: stats_aggregated_playlist_day_current_count_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_aggregated_playlist_day_current_count_idx ON public.stats_aggregated_playlist USING btree (day_current_count);


--
-- TOC entry 5991 (class 1259 OID 26676)
-- Name: stats_aggregated_playlist_month_current_count_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_aggregated_playlist_month_current_count_idx ON public.stats_aggregated_playlist USING btree (month_current_count);


--
-- TOC entry 5994 (class 1259 OID 26673)
-- Name: stats_aggregated_playlist_playlist_id_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_aggregated_playlist_playlist_id_idx ON public.stats_aggregated_playlist USING btree (playlist_id);


--
-- TOC entry 5997 (class 1259 OID 26675)
-- Name: stats_aggregated_playlist_week_current_count_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_aggregated_playlist_week_current_count_idx ON public.stats_aggregated_playlist USING btree (week_current_count);


--
-- TOC entry 5925 (class 1259 OID 26444)
-- Name: stats_track_account_guid_account_guid_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_track_account_guid_account_guid_idx ON public.stats_track_account_guid USING btree (account_guid);


--
-- TOC entry 5928 (class 1259 OID 26443)
-- Name: stats_track_account_guid_account_id_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_track_account_guid_account_id_idx ON public.stats_track_account_guid USING btree (account_id);


--
-- TOC entry 5933 (class 1259 OID 26445)
-- Name: stats_track_account_guid_updated_at_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_track_account_guid_updated_at_idx ON public.stats_track_account_guid USING btree (updated_at);


--
-- TOC entry 5998 (class 1259 OID 26697)
-- Name: stats_track_event_account_account_guid_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_track_event_account_account_guid_idx ON public.stats_track_event_account USING btree (account_guid);


--
-- TOC entry 6001 (class 1259 OID 26699)
-- Name: stats_track_event_account_created_at_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_track_event_account_created_at_idx ON public.stats_track_event_account USING btree (created_at);


--
-- TOC entry 6004 (class 1259 OID 26698)
-- Name: stats_track_event_account_tracked_account_id_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_track_event_account_tracked_account_id_idx ON public.stats_track_event_account USING btree (tracked_account_id);


--
-- TOC entry 5936 (class 1259 OID 26465)
-- Name: stats_track_event_channel_account_guid_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_track_event_channel_account_guid_idx ON public.stats_track_event_channel USING btree (account_guid);


--
-- TOC entry 5937 (class 1259 OID 26466)
-- Name: stats_track_event_channel_channel_id_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_track_event_channel_channel_id_idx ON public.stats_track_event_channel USING btree (channel_id);


--
-- TOC entry 5938 (class 1259 OID 26467)
-- Name: stats_track_event_channel_created_at_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_track_event_channel_created_at_idx ON public.stats_track_event_channel USING btree (created_at);


--
-- TOC entry 5968 (class 1259 OID 26581)
-- Name: stats_track_event_clip_account_guid_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_track_event_clip_account_guid_idx ON public.stats_track_event_clip USING btree (account_guid);


--
-- TOC entry 5969 (class 1259 OID 26582)
-- Name: stats_track_event_clip_clip_id_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_track_event_clip_clip_id_idx ON public.stats_track_event_clip USING btree (clip_id);


--
-- TOC entry 5970 (class 1259 OID 26583)
-- Name: stats_track_event_clip_created_at_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_track_event_clip_created_at_idx ON public.stats_track_event_clip USING btree (created_at);


--
-- TOC entry 5950 (class 1259 OID 26523)
-- Name: stats_track_event_item_account_guid_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_track_event_item_account_guid_idx ON public.stats_track_event_item USING btree (account_guid);


--
-- TOC entry 5953 (class 1259 OID 26525)
-- Name: stats_track_event_item_created_at_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_track_event_item_created_at_idx ON public.stats_track_event_item USING btree (created_at);


--
-- TOC entry 5954 (class 1259 OID 26524)
-- Name: stats_track_event_item_item_id_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_track_event_item_item_id_idx ON public.stats_track_event_item USING btree (item_id);


--
-- TOC entry 5982 (class 1259 OID 26639)
-- Name: stats_track_event_playlist_account_guid_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_track_event_playlist_account_guid_idx ON public.stats_track_event_playlist USING btree (account_guid);


--
-- TOC entry 5985 (class 1259 OID 26641)
-- Name: stats_track_event_playlist_created_at_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_track_event_playlist_created_at_idx ON public.stats_track_event_playlist USING btree (created_at);


--
-- TOC entry 5988 (class 1259 OID 26640)
-- Name: stats_track_event_playlist_playlist_id_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX stats_track_event_playlist_playlist_id_idx ON public.stats_track_event_playlist USING btree (playlist_id);


--
-- TOC entry 6140 (class 2620 OID 26173)
-- Name: playlist_resource delete_playlist_resource_trigger; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER delete_playlist_resource_trigger BEFORE DELETE ON public.playlist_resource FOR EACH ROW EXECUTE FUNCTION public.delete_playlist_resource();


--
-- TOC entry 6138 (class 2620 OID 24907)
-- Name: feed set_updated_at_feed; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER set_updated_at_feed BEFORE UPDATE ON public.feed FOR EACH ROW EXECUTE FUNCTION public.set_updated_at_field();


--
-- TOC entry 6137 (class 2620 OID 24887)
-- Name: feed_flag_status set_updated_at_feed_flag_status; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER set_updated_at_feed_flag_status BEFORE UPDATE ON public.feed_flag_status FOR EACH ROW EXECUTE FUNCTION public.set_updated_at_field();


--
-- TOC entry 6139 (class 2620 OID 25359)
-- Name: item_flag_status set_updated_at_item_flag_status; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER set_updated_at_item_flag_status BEFORE UPDATE ON public.item_flag_status FOR EACH ROW EXECUTE FUNCTION public.set_updated_at_field();


--
-- TOC entry 6087 (class 2606 OID 26052)
-- Name: account_admin_roles account_admin_roles_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_admin_roles
    ADD CONSTRAINT account_admin_roles_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.account(id) ON DELETE CASCADE;


--
-- TOC entry 6118 (class 2606 OID 26392)
-- Name: account_app_store_purchase account_app_store_purchase_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_app_store_purchase
    ADD CONSTRAINT account_app_store_purchase_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.account(id) ON DELETE CASCADE;


--
-- TOC entry 6080 (class 2606 OID 25934)
-- Name: account_credentials account_credentials_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_credentials
    ADD CONSTRAINT account_credentials_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.account(id) ON DELETE CASCADE;


--
-- TOC entry 6084 (class 2606 OID 26002)
-- Name: account_email_change_verification account_email_change_verification_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_email_change_verification
    ADD CONSTRAINT account_email_change_verification_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.account(id) ON DELETE CASCADE;


--
-- TOC entry 6116 (class 2606 OID 26365)
-- Name: account_fcm_device account_fcm_device_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_fcm_device
    ADD CONSTRAINT account_fcm_device_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.account(id) ON DELETE CASCADE;


--
-- TOC entry 6106 (class 2606 OID 26260)
-- Name: account_following_account account_following_account_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_following_account
    ADD CONSTRAINT account_following_account_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.account(id) ON DELETE CASCADE;


--
-- TOC entry 6107 (class 2606 OID 26265)
-- Name: account_following_account account_following_account_following_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_following_account
    ADD CONSTRAINT account_following_account_following_account_id_fkey FOREIGN KEY (following_account_id) REFERENCES public.account(id) ON DELETE CASCADE;


--
-- TOC entry 6112 (class 2606 OID 26313)
-- Name: account_following_add_by_rss_channel account_following_add_by_rss_channel_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_following_add_by_rss_channel
    ADD CONSTRAINT account_following_add_by_rss_channel_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.account(id) ON DELETE CASCADE;


--
-- TOC entry 6108 (class 2606 OID 26277)
-- Name: account_following_channel account_following_channel_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_following_channel
    ADD CONSTRAINT account_following_channel_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.account(id) ON DELETE CASCADE;


--
-- TOC entry 6109 (class 2606 OID 26282)
-- Name: account_following_channel account_following_channel_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_following_channel
    ADD CONSTRAINT account_following_channel_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.channel(id) ON DELETE CASCADE;


--
-- TOC entry 6110 (class 2606 OID 26294)
-- Name: account_following_playlist account_following_playlist_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_following_playlist
    ADD CONSTRAINT account_following_playlist_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.account(id) ON DELETE CASCADE;


--
-- TOC entry 6111 (class 2606 OID 26299)
-- Name: account_following_playlist account_following_playlist_playlist_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_following_playlist
    ADD CONSTRAINT account_following_playlist_playlist_id_fkey FOREIGN KEY (playlist_id) REFERENCES public.playlist(id) ON DELETE CASCADE;


--
-- TOC entry 6119 (class 2606 OID 26407)
-- Name: account_google_play_purchase account_google_play_purchase_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_google_play_purchase
    ADD CONSTRAINT account_google_play_purchase_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.account(id) ON DELETE CASCADE;


--
-- TOC entry 6085 (class 2606 OID 26029)
-- Name: account_membership_status account_membership_status_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_membership_status
    ADD CONSTRAINT account_membership_status_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.account(id) ON DELETE CASCADE;


--
-- TOC entry 6086 (class 2606 OID 26034)
-- Name: account_membership_status account_membership_status_account_membership_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_membership_status
    ADD CONSTRAINT account_membership_status_account_membership_id_fkey FOREIGN KEY (account_membership_id) REFERENCES public.account_membership(id);


--
-- TOC entry 6113 (class 2606 OID 26329)
-- Name: account_notification_channel account_notification_channel_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_notification_channel
    ADD CONSTRAINT account_notification_channel_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.account(id) ON DELETE CASCADE;


--
-- TOC entry 6114 (class 2606 OID 26324)
-- Name: account_notification_channel account_notification_channel_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_notification_channel
    ADD CONSTRAINT account_notification_channel_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.channel(id) ON DELETE CASCADE;


--
-- TOC entry 6117 (class 2606 OID 26379)
-- Name: account_paypal_order account_paypal_order_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_paypal_order
    ADD CONSTRAINT account_paypal_order_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.account(id) ON DELETE CASCADE;


--
-- TOC entry 6081 (class 2606 OID 25951)
-- Name: account_profile account_profile_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_profile
    ADD CONSTRAINT account_profile_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.account(id) ON DELETE CASCADE;


--
-- TOC entry 6082 (class 2606 OID 25968)
-- Name: account_reset_password account_reset_password_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_reset_password
    ADD CONSTRAINT account_reset_password_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.account(id) ON DELETE CASCADE;


--
-- TOC entry 6079 (class 2606 OID 25915)
-- Name: account account_sharable_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account
    ADD CONSTRAINT account_sharable_status_id_fkey FOREIGN KEY (sharable_status_id) REFERENCES public.sharable_status(id);


--
-- TOC entry 6115 (class 2606 OID 26347)
-- Name: account_up_device account_up_device_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_up_device
    ADD CONSTRAINT account_up_device_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.account(id) ON DELETE CASCADE;


--
-- TOC entry 6083 (class 2606 OID 25985)
-- Name: account_verification account_verification_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_verification
    ADD CONSTRAINT account_verification_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.account(id) ON DELETE CASCADE;


--
-- TOC entry 6014 (class 2606 OID 24857)
-- Name: category category_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.category
    ADD CONSTRAINT category_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.category(id) ON DELETE CASCADE;


--
-- TOC entry 6019 (class 2606 OID 24980)
-- Name: channel_about channel_about_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_about
    ADD CONSTRAINT channel_about_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.channel(id) ON DELETE CASCADE;


--
-- TOC entry 6020 (class 2606 OID 24985)
-- Name: channel_about channel_about_itunes_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_about
    ADD CONSTRAINT channel_about_itunes_type_id_fkey FOREIGN KEY (itunes_type_id) REFERENCES public.channel_itunes_type(id);


--
-- TOC entry 6021 (class 2606 OID 25004)
-- Name: channel_category channel_category_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_category
    ADD CONSTRAINT channel_category_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.category(id) ON DELETE CASCADE;


--
-- TOC entry 6022 (class 2606 OID 24999)
-- Name: channel_category channel_category_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_category
    ADD CONSTRAINT channel_category_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.channel(id) ON DELETE CASCADE;


--
-- TOC entry 6023 (class 2606 OID 25022)
-- Name: channel_chat channel_chat_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_chat
    ADD CONSTRAINT channel_chat_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.channel(id) ON DELETE CASCADE;


--
-- TOC entry 6024 (class 2606 OID 25039)
-- Name: channel_description channel_description_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_description
    ADD CONSTRAINT channel_description_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.channel(id) ON DELETE CASCADE;


--
-- TOC entry 6017 (class 2606 OID 24943)
-- Name: channel channel_feed_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel
    ADD CONSTRAINT channel_feed_id_fkey FOREIGN KEY (feed_id) REFERENCES public.feed(id) ON DELETE CASCADE;


--
-- TOC entry 6025 (class 2606 OID 25054)
-- Name: channel_funding channel_funding_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_funding
    ADD CONSTRAINT channel_funding_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.channel(id) ON DELETE CASCADE;


--
-- TOC entry 6026 (class 2606 OID 25070)
-- Name: channel_image channel_image_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_image
    ADD CONSTRAINT channel_image_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.channel(id) ON DELETE CASCADE;


--
-- TOC entry 6027 (class 2606 OID 25085)
-- Name: channel_internal_settings channel_internal_settings_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_internal_settings
    ADD CONSTRAINT channel_internal_settings_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.channel(id) ON DELETE CASCADE;


--
-- TOC entry 6028 (class 2606 OID 25102)
-- Name: channel_license channel_license_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_license
    ADD CONSTRAINT channel_license_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.channel(id) ON DELETE CASCADE;


--
-- TOC entry 6029 (class 2606 OID 25120)
-- Name: channel_location channel_location_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_location
    ADD CONSTRAINT channel_location_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.channel(id) ON DELETE CASCADE;


--
-- TOC entry 6018 (class 2606 OID 24948)
-- Name: channel channel_medium_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel
    ADD CONSTRAINT channel_medium_id_fkey FOREIGN KEY (medium_id) REFERENCES public.medium(id);


--
-- TOC entry 6030 (class 2606 OID 25136)
-- Name: channel_person channel_person_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_person
    ADD CONSTRAINT channel_person_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.channel(id) ON DELETE CASCADE;


--
-- TOC entry 6031 (class 2606 OID 25151)
-- Name: channel_podroll channel_podroll_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_podroll
    ADD CONSTRAINT channel_podroll_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.channel(id) ON DELETE CASCADE;


--
-- TOC entry 6032 (class 2606 OID 25166)
-- Name: channel_podroll_remote_item channel_podroll_remote_item_channel_podroll_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_podroll_remote_item
    ADD CONSTRAINT channel_podroll_remote_item_channel_podroll_id_fkey FOREIGN KEY (channel_podroll_id) REFERENCES public.channel_podroll(id) ON DELETE CASCADE;


--
-- TOC entry 6033 (class 2606 OID 25171)
-- Name: channel_podroll_remote_item channel_podroll_remote_item_medium_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_podroll_remote_item
    ADD CONSTRAINT channel_podroll_remote_item_medium_id_fkey FOREIGN KEY (medium_id) REFERENCES public.medium(id);


--
-- TOC entry 6034 (class 2606 OID 25190)
-- Name: channel_publisher channel_publisher_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_publisher
    ADD CONSTRAINT channel_publisher_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.channel(id) ON DELETE CASCADE;


--
-- TOC entry 6035 (class 2606 OID 25207)
-- Name: channel_publisher_remote_item channel_publisher_remote_item_channel_publisher_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_publisher_remote_item
    ADD CONSTRAINT channel_publisher_remote_item_channel_publisher_id_fkey FOREIGN KEY (channel_publisher_id) REFERENCES public.channel_publisher(id) ON DELETE CASCADE;


--
-- TOC entry 6036 (class 2606 OID 25212)
-- Name: channel_publisher_remote_item channel_publisher_remote_item_medium_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_publisher_remote_item
    ADD CONSTRAINT channel_publisher_remote_item_medium_id_fkey FOREIGN KEY (medium_id) REFERENCES public.medium(id);


--
-- TOC entry 6037 (class 2606 OID 25231)
-- Name: channel_remote_item channel_remote_item_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_remote_item
    ADD CONSTRAINT channel_remote_item_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.channel(id) ON DELETE CASCADE;


--
-- TOC entry 6038 (class 2606 OID 25236)
-- Name: channel_remote_item channel_remote_item_medium_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_remote_item
    ADD CONSTRAINT channel_remote_item_medium_id_fkey FOREIGN KEY (medium_id) REFERENCES public.medium(id);


--
-- TOC entry 6039 (class 2606 OID 25257)
-- Name: channel_season channel_season_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_season
    ADD CONSTRAINT channel_season_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.channel(id) ON DELETE CASCADE;


--
-- TOC entry 6040 (class 2606 OID 25272)
-- Name: channel_social_interact channel_social_interact_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_social_interact
    ADD CONSTRAINT channel_social_interact_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.channel(id) ON DELETE CASCADE;


--
-- TOC entry 6041 (class 2606 OID 25289)
-- Name: channel_trailer channel_trailer_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_trailer
    ADD CONSTRAINT channel_trailer_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.channel(id) ON DELETE CASCADE;


--
-- TOC entry 6042 (class 2606 OID 25294)
-- Name: channel_trailer channel_trailer_channel_season_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_trailer
    ADD CONSTRAINT channel_trailer_channel_season_id_fkey FOREIGN KEY (channel_season_id) REFERENCES public.channel_season(id);


--
-- TOC entry 6043 (class 2606 OID 25310)
-- Name: channel_txt channel_txt_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_txt
    ADD CONSTRAINT channel_txt_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.channel(id) ON DELETE CASCADE;


--
-- TOC entry 6044 (class 2606 OID 25325)
-- Name: channel_value channel_value_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_value
    ADD CONSTRAINT channel_value_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.channel(id) ON DELETE CASCADE;


--
-- TOC entry 6045 (class 2606 OID 25341)
-- Name: channel_value_recipient channel_value_recipient_channel_value_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.channel_value_recipient
    ADD CONSTRAINT channel_value_recipient_channel_value_id_fkey FOREIGN KEY (channel_value_id) REFERENCES public.channel_value(id) ON DELETE CASCADE;


--
-- TOC entry 6088 (class 2606 OID 26069)
-- Name: clip clip_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clip
    ADD CONSTRAINT clip_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.account(id) ON DELETE CASCADE;


--
-- TOC entry 6089 (class 2606 OID 26074)
-- Name: clip clip_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clip
    ADD CONSTRAINT clip_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.item(id) ON DELETE CASCADE;


--
-- TOC entry 6090 (class 2606 OID 26079)
-- Name: clip clip_sharable_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clip
    ADD CONSTRAINT clip_sharable_status_id_fkey FOREIGN KEY (sharable_status_id) REFERENCES public.sharable_status(id);


--
-- TOC entry 6015 (class 2606 OID 24901)
-- Name: feed feed_feed_flag_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.feed
    ADD CONSTRAINT feed_feed_flag_status_id_fkey FOREIGN KEY (feed_flag_status_id) REFERENCES public.feed_flag_status(id);


--
-- TOC entry 6016 (class 2606 OID 24918)
-- Name: feed_log feed_log_feed_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.feed_log
    ADD CONSTRAINT feed_log_feed_id_fkey FOREIGN KEY (feed_id) REFERENCES public.feed(id) ON DELETE CASCADE;


--
-- TOC entry 6048 (class 2606 OID 25410)
-- Name: item_about item_about_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_about
    ADD CONSTRAINT item_about_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.item(id) ON DELETE CASCADE;


--
-- TOC entry 6049 (class 2606 OID 25415)
-- Name: item_about item_about_item_itunes_episode_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_about
    ADD CONSTRAINT item_about_item_itunes_episode_type_id_fkey FOREIGN KEY (item_itunes_episode_type_id) REFERENCES public.item_itunes_episode_type(id);


--
-- TOC entry 6046 (class 2606 OID 25372)
-- Name: item item_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item
    ADD CONSTRAINT item_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.channel(id) ON DELETE CASCADE;


--
-- TOC entry 6052 (class 2606 OID 25467)
-- Name: item_chapter item_chapter_item_chapters_feed_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_chapter
    ADD CONSTRAINT item_chapter_item_chapters_feed_id_fkey FOREIGN KEY (item_chapters_feed_id) REFERENCES public.item_chapters_feed(id) ON DELETE CASCADE;


--
-- TOC entry 6053 (class 2606 OID 25485)
-- Name: item_chapter_location item_chapter_location_item_chapter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_chapter_location
    ADD CONSTRAINT item_chapter_location_item_chapter_id_fkey FOREIGN KEY (item_chapter_id) REFERENCES public.item_chapter(id) ON DELETE CASCADE;


--
-- TOC entry 6050 (class 2606 OID 25433)
-- Name: item_chapters_feed item_chapters_feed_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_chapters_feed
    ADD CONSTRAINT item_chapters_feed_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.item(id) ON DELETE CASCADE;


--
-- TOC entry 6051 (class 2606 OID 25449)
-- Name: item_chapters_feed_log item_chapters_feed_log_item_chapters_feed_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_chapters_feed_log
    ADD CONSTRAINT item_chapters_feed_log_item_chapters_feed_id_fkey FOREIGN KEY (item_chapters_feed_id) REFERENCES public.item_chapters_feed(id) ON DELETE CASCADE;


--
-- TOC entry 6054 (class 2606 OID 25502)
-- Name: item_chat item_chat_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_chat
    ADD CONSTRAINT item_chat_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.item(id) ON DELETE CASCADE;


--
-- TOC entry 6055 (class 2606 OID 25517)
-- Name: item_content_link item_content_link_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_content_link
    ADD CONSTRAINT item_content_link_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.item(id) ON DELETE CASCADE;


--
-- TOC entry 6056 (class 2606 OID 25534)
-- Name: item_description item_description_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_description
    ADD CONSTRAINT item_description_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.item(id) ON DELETE CASCADE;


--
-- TOC entry 6059 (class 2606 OID 25583)
-- Name: item_enclosure_integrity item_enclosure_integrity_item_enclosure_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_enclosure_integrity
    ADD CONSTRAINT item_enclosure_integrity_item_enclosure_id_fkey FOREIGN KEY (item_enclosure_id) REFERENCES public.item_enclosure(id) ON DELETE CASCADE;


--
-- TOC entry 6057 (class 2606 OID 25550)
-- Name: item_enclosure item_enclosure_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_enclosure
    ADD CONSTRAINT item_enclosure_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.item(id) ON DELETE CASCADE;


--
-- TOC entry 6058 (class 2606 OID 25565)
-- Name: item_enclosure_source item_enclosure_source_item_enclosure_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_enclosure_source
    ADD CONSTRAINT item_enclosure_source_item_enclosure_id_fkey FOREIGN KEY (item_enclosure_id) REFERENCES public.item_enclosure(id) ON DELETE CASCADE;


--
-- TOC entry 6060 (class 2606 OID 25598)
-- Name: item_funding item_funding_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_funding
    ADD CONSTRAINT item_funding_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.item(id) ON DELETE CASCADE;


--
-- TOC entry 6061 (class 2606 OID 25614)
-- Name: item_image item_image_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_image
    ADD CONSTRAINT item_image_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.item(id) ON DELETE CASCADE;


--
-- TOC entry 6047 (class 2606 OID 25377)
-- Name: item item_item_flag_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item
    ADD CONSTRAINT item_item_flag_status_id_fkey FOREIGN KEY (item_flag_status_id) REFERENCES public.item_flag_status(id);


--
-- TOC entry 6062 (class 2606 OID 25631)
-- Name: item_license item_license_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_license
    ADD CONSTRAINT item_license_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.item(id) ON DELETE CASCADE;


--
-- TOC entry 6063 (class 2606 OID 25649)
-- Name: item_location item_location_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_location
    ADD CONSTRAINT item_location_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.item(id) ON DELETE CASCADE;


--
-- TOC entry 6064 (class 2606 OID 25665)
-- Name: item_person item_person_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_person
    ADD CONSTRAINT item_person_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.item(id) ON DELETE CASCADE;


--
-- TOC entry 6065 (class 2606 OID 25680)
-- Name: item_season item_season_channel_season_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_season
    ADD CONSTRAINT item_season_channel_season_id_fkey FOREIGN KEY (channel_season_id) REFERENCES public.channel_season(id) ON DELETE CASCADE;


--
-- TOC entry 6067 (class 2606 OID 25703)
-- Name: item_season_episode item_season_episode_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_season_episode
    ADD CONSTRAINT item_season_episode_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.item(id) ON DELETE CASCADE;


--
-- TOC entry 6066 (class 2606 OID 25685)
-- Name: item_season item_season_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_season
    ADD CONSTRAINT item_season_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.item(id) ON DELETE CASCADE;


--
-- TOC entry 6068 (class 2606 OID 25718)
-- Name: item_social_interact item_social_interact_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_social_interact
    ADD CONSTRAINT item_social_interact_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.item(id) ON DELETE CASCADE;


--
-- TOC entry 6069 (class 2606 OID 25735)
-- Name: item_soundbite item_soundbite_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_soundbite
    ADD CONSTRAINT item_soundbite_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.item(id) ON DELETE CASCADE;


--
-- TOC entry 6070 (class 2606 OID 25751)
-- Name: item_transcript item_transcript_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_transcript
    ADD CONSTRAINT item_transcript_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.item(id) ON DELETE CASCADE;


--
-- TOC entry 6071 (class 2606 OID 25766)
-- Name: item_txt item_txt_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_txt
    ADD CONSTRAINT item_txt_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.item(id) ON DELETE CASCADE;


--
-- TOC entry 6072 (class 2606 OID 25781)
-- Name: item_value item_value_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_value
    ADD CONSTRAINT item_value_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.item(id) ON DELETE CASCADE;


--
-- TOC entry 6073 (class 2606 OID 25797)
-- Name: item_value_recipient item_value_recipient_item_value_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_value_recipient
    ADD CONSTRAINT item_value_recipient_item_value_id_fkey FOREIGN KEY (item_value_id) REFERENCES public.item_value(id) ON DELETE CASCADE;


--
-- TOC entry 6074 (class 2606 OID 25814)
-- Name: item_value_time_split item_value_time_split_item_value_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_value_time_split
    ADD CONSTRAINT item_value_time_split_item_value_id_fkey FOREIGN KEY (item_value_id) REFERENCES public.item_value(id) ON DELETE CASCADE;


--
-- TOC entry 6076 (class 2606 OID 25850)
-- Name: item_value_time_split_recipient item_value_time_split_recipient_item_value_time_split_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_value_time_split_recipient
    ADD CONSTRAINT item_value_time_split_recipient_item_value_time_split_id_fkey FOREIGN KEY (item_value_time_split_id) REFERENCES public.item_value_time_split(id) ON DELETE CASCADE;


--
-- TOC entry 6075 (class 2606 OID 25831)
-- Name: item_value_time_split_remote_item item_value_time_split_remote_item_item_value_time_split_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_value_time_split_remote_item
    ADD CONSTRAINT item_value_time_split_remote_item_item_value_time_split_id_fkey FOREIGN KEY (item_value_time_split_id) REFERENCES public.item_value_time_split(id) ON DELETE CASCADE;


--
-- TOC entry 6077 (class 2606 OID 25879)
-- Name: live_item live_item_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.live_item
    ADD CONSTRAINT live_item_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.item(id) ON DELETE CASCADE;


--
-- TOC entry 6078 (class 2606 OID 25884)
-- Name: live_item live_item_live_item_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.live_item
    ADD CONSTRAINT live_item_live_item_status_id_fkey FOREIGN KEY (live_item_status_id) REFERENCES public.live_item_status(id);


--
-- TOC entry 6120 (class 2606 OID 26421)
-- Name: membership_claim_token membership_claim_token_account_membership_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.membership_claim_token
    ADD CONSTRAINT membership_claim_token_account_membership_id_fkey FOREIGN KEY (account_membership_id) REFERENCES public.account_membership(id) ON DELETE CASCADE;


--
-- TOC entry 6091 (class 2606 OID 26100)
-- Name: playlist playlist_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.playlist
    ADD CONSTRAINT playlist_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.account(id) ON DELETE CASCADE;


--
-- TOC entry 6092 (class 2606 OID 26110)
-- Name: playlist playlist_medium_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.playlist
    ADD CONSTRAINT playlist_medium_id_fkey FOREIGN KEY (medium_id) REFERENCES public.medium(id);


--
-- TOC entry 6094 (class 2606 OID 26156)
-- Name: playlist_resource playlist_resource_clip_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.playlist_resource
    ADD CONSTRAINT playlist_resource_clip_id_fkey FOREIGN KEY (clip_id) REFERENCES public.clip(id) ON DELETE CASCADE;


--
-- TOC entry 6095 (class 2606 OID 26151)
-- Name: playlist_resource playlist_resource_item_chapter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.playlist_resource
    ADD CONSTRAINT playlist_resource_item_chapter_id_fkey FOREIGN KEY (item_chapter_id) REFERENCES public.item_chapter(id) ON DELETE CASCADE;


--
-- TOC entry 6096 (class 2606 OID 26146)
-- Name: playlist_resource playlist_resource_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.playlist_resource
    ADD CONSTRAINT playlist_resource_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.item(id) ON DELETE CASCADE;


--
-- TOC entry 6097 (class 2606 OID 26161)
-- Name: playlist_resource playlist_resource_item_soundbite_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.playlist_resource
    ADD CONSTRAINT playlist_resource_item_soundbite_id_fkey FOREIGN KEY (item_soundbite_id) REFERENCES public.item_soundbite(id) ON DELETE CASCADE;


--
-- TOC entry 6098 (class 2606 OID 26141)
-- Name: playlist_resource playlist_resource_playlist_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.playlist_resource
    ADD CONSTRAINT playlist_resource_playlist_id_fkey FOREIGN KEY (playlist_id) REFERENCES public.playlist(id) ON DELETE CASCADE;


--
-- TOC entry 6093 (class 2606 OID 26105)
-- Name: playlist playlist_sharable_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.playlist
    ADD CONSTRAINT playlist_sharable_status_id_fkey FOREIGN KEY (sharable_status_id) REFERENCES public.sharable_status(id);


--
-- TOC entry 6099 (class 2606 OID 26187)
-- Name: queue queue_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.queue
    ADD CONSTRAINT queue_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.account(id) ON DELETE CASCADE;


--
-- TOC entry 6100 (class 2606 OID 26192)
-- Name: queue queue_medium_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.queue
    ADD CONSTRAINT queue_medium_id_fkey FOREIGN KEY (medium_id) REFERENCES public.medium(id);


--
-- TOC entry 6101 (class 2606 OID 26239)
-- Name: queue_resource queue_resource_clip_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.queue_resource
    ADD CONSTRAINT queue_resource_clip_id_fkey FOREIGN KEY (clip_id) REFERENCES public.clip(id) ON DELETE CASCADE;


--
-- TOC entry 6102 (class 2606 OID 26234)
-- Name: queue_resource queue_resource_item_chapter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.queue_resource
    ADD CONSTRAINT queue_resource_item_chapter_id_fkey FOREIGN KEY (item_chapter_id) REFERENCES public.item_chapter(id) ON DELETE CASCADE;


--
-- TOC entry 6103 (class 2606 OID 26229)
-- Name: queue_resource queue_resource_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.queue_resource
    ADD CONSTRAINT queue_resource_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.item(id) ON DELETE CASCADE;


--
-- TOC entry 6104 (class 2606 OID 26244)
-- Name: queue_resource queue_resource_item_soundbite_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.queue_resource
    ADD CONSTRAINT queue_resource_item_soundbite_id_fkey FOREIGN KEY (item_soundbite_id) REFERENCES public.item_soundbite(id) ON DELETE CASCADE;


--
-- TOC entry 6105 (class 2606 OID 26224)
-- Name: queue_resource queue_resource_queue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.queue_resource
    ADD CONSTRAINT queue_resource_queue_id_fkey FOREIGN KEY (queue_id) REFERENCES public.queue(id) ON DELETE CASCADE;


--
-- TOC entry 6136 (class 2606 OID 26726)
-- Name: stats_aggregated_account stats_aggregated_account_tracked_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_aggregated_account
    ADD CONSTRAINT stats_aggregated_account_tracked_account_id_fkey FOREIGN KEY (tracked_account_id) REFERENCES public.account(id) ON DELETE CASCADE;


--
-- TOC entry 6124 (class 2606 OID 26494)
-- Name: stats_aggregated_channel stats_aggregated_channel_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_aggregated_channel
    ADD CONSTRAINT stats_aggregated_channel_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.channel(id) ON DELETE CASCADE;


--
-- TOC entry 6130 (class 2606 OID 26610)
-- Name: stats_aggregated_clip stats_aggregated_clip_clip_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_aggregated_clip
    ADD CONSTRAINT stats_aggregated_clip_clip_id_fkey FOREIGN KEY (clip_id) REFERENCES public.clip(id) ON DELETE CASCADE;


--
-- TOC entry 6127 (class 2606 OID 26552)
-- Name: stats_aggregated_item stats_aggregated_item_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_aggregated_item
    ADD CONSTRAINT stats_aggregated_item_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.item(id) ON DELETE CASCADE;


--
-- TOC entry 6133 (class 2606 OID 26668)
-- Name: stats_aggregated_playlist stats_aggregated_playlist_playlist_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_aggregated_playlist
    ADD CONSTRAINT stats_aggregated_playlist_playlist_id_fkey FOREIGN KEY (playlist_id) REFERENCES public.playlist(id) ON DELETE CASCADE;


--
-- TOC entry 6121 (class 2606 OID 26438)
-- Name: stats_track_account_guid stats_track_account_guid_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_account_guid
    ADD CONSTRAINT stats_track_account_guid_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.account(id) ON DELETE CASCADE;


--
-- TOC entry 6134 (class 2606 OID 26687)
-- Name: stats_track_event_account stats_track_event_account_account_guid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_event_account
    ADD CONSTRAINT stats_track_event_account_account_guid_fkey FOREIGN KEY (account_guid) REFERENCES public.stats_track_account_guid(account_guid) ON DELETE CASCADE;


--
-- TOC entry 6135 (class 2606 OID 26692)
-- Name: stats_track_event_account stats_track_event_account_tracked_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_event_account
    ADD CONSTRAINT stats_track_event_account_tracked_account_id_fkey FOREIGN KEY (tracked_account_id) REFERENCES public.account(id) ON DELETE CASCADE;


--
-- TOC entry 6122 (class 2606 OID 26455)
-- Name: stats_track_event_channel stats_track_event_channel_account_guid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_event_channel
    ADD CONSTRAINT stats_track_event_channel_account_guid_fkey FOREIGN KEY (account_guid) REFERENCES public.stats_track_account_guid(account_guid) ON DELETE CASCADE;


--
-- TOC entry 6123 (class 2606 OID 26460)
-- Name: stats_track_event_channel stats_track_event_channel_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_event_channel
    ADD CONSTRAINT stats_track_event_channel_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.channel(id) ON DELETE CASCADE;


--
-- TOC entry 6128 (class 2606 OID 26571)
-- Name: stats_track_event_clip stats_track_event_clip_account_guid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_event_clip
    ADD CONSTRAINT stats_track_event_clip_account_guid_fkey FOREIGN KEY (account_guid) REFERENCES public.stats_track_account_guid(account_guid) ON DELETE CASCADE;


--
-- TOC entry 6129 (class 2606 OID 26576)
-- Name: stats_track_event_clip stats_track_event_clip_clip_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_event_clip
    ADD CONSTRAINT stats_track_event_clip_clip_id_fkey FOREIGN KEY (clip_id) REFERENCES public.clip(id) ON DELETE CASCADE;


--
-- TOC entry 6125 (class 2606 OID 26513)
-- Name: stats_track_event_item stats_track_event_item_account_guid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_event_item
    ADD CONSTRAINT stats_track_event_item_account_guid_fkey FOREIGN KEY (account_guid) REFERENCES public.stats_track_account_guid(account_guid) ON DELETE CASCADE;


--
-- TOC entry 6126 (class 2606 OID 26518)
-- Name: stats_track_event_item stats_track_event_item_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_event_item
    ADD CONSTRAINT stats_track_event_item_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.item(id) ON DELETE CASCADE;


--
-- TOC entry 6131 (class 2606 OID 26629)
-- Name: stats_track_event_playlist stats_track_event_playlist_account_guid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_event_playlist
    ADD CONSTRAINT stats_track_event_playlist_account_guid_fkey FOREIGN KEY (account_guid) REFERENCES public.stats_track_account_guid(account_guid) ON DELETE CASCADE;


--
-- TOC entry 6132 (class 2606 OID 26634)
-- Name: stats_track_event_playlist stats_track_event_playlist_playlist_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stats_track_event_playlist
    ADD CONSTRAINT stats_track_event_playlist_playlist_id_fkey FOREIGN KEY (playlist_id) REFERENCES public.playlist(id) ON DELETE CASCADE;


--
-- TOC entry 6476 (class 0 OID 0)
-- Dependencies: 5
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT USAGE ON SCHEMA public TO admin;
GRANT USAGE ON SCHEMA public TO read;
GRANT USAGE ON SCHEMA public TO read_write;


--
-- TOC entry 6477 (class 0 OID 0)
-- Dependencies: 340
-- Name: TABLE account; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.account TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.account TO read_write;


--
-- TOC entry 6478 (class 0 OID 0)
-- Dependencies: 356
-- Name: TABLE account_admin_roles; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.account_admin_roles TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.account_admin_roles TO read_write;


--
-- TOC entry 6480 (class 0 OID 0)
-- Dependencies: 355
-- Name: SEQUENCE account_admin_roles_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.account_admin_roles_id_seq TO read;
GRANT ALL ON SEQUENCE public.account_admin_roles_id_seq TO read_write;


--
-- TOC entry 6481 (class 0 OID 0)
-- Dependencies: 377
-- Name: TABLE account_app_store_purchase; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.account_app_store_purchase TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.account_app_store_purchase TO read_write;


--
-- TOC entry 6482 (class 0 OID 0)
-- Dependencies: 342
-- Name: TABLE account_credentials; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.account_credentials TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.account_credentials TO read_write;


--
-- TOC entry 6484 (class 0 OID 0)
-- Dependencies: 341
-- Name: SEQUENCE account_credentials_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.account_credentials_id_seq TO read;
GRANT ALL ON SEQUENCE public.account_credentials_id_seq TO read_write;


--
-- TOC entry 6485 (class 0 OID 0)
-- Dependencies: 350
-- Name: TABLE account_email_change_verification; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.account_email_change_verification TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.account_email_change_verification TO read_write;


--
-- TOC entry 6487 (class 0 OID 0)
-- Dependencies: 349
-- Name: SEQUENCE account_email_change_verification_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.account_email_change_verification_id_seq TO read;
GRANT ALL ON SEQUENCE public.account_email_change_verification_id_seq TO read_write;


--
-- TOC entry 6488 (class 0 OID 0)
-- Dependencies: 375
-- Name: TABLE account_fcm_device; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.account_fcm_device TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.account_fcm_device TO read_write;


--
-- TOC entry 6490 (class 0 OID 0)
-- Dependencies: 374
-- Name: SEQUENCE account_fcm_device_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.account_fcm_device_id_seq TO read;
GRANT ALL ON SEQUENCE public.account_fcm_device_id_seq TO read_write;


--
-- TOC entry 6491 (class 0 OID 0)
-- Dependencies: 367
-- Name: TABLE account_following_account; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.account_following_account TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.account_following_account TO read_write;


--
-- TOC entry 6492 (class 0 OID 0)
-- Dependencies: 370
-- Name: TABLE account_following_add_by_rss_channel; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.account_following_add_by_rss_channel TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.account_following_add_by_rss_channel TO read_write;


--
-- TOC entry 6493 (class 0 OID 0)
-- Dependencies: 368
-- Name: TABLE account_following_channel; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.account_following_channel TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.account_following_channel TO read_write;


--
-- TOC entry 6494 (class 0 OID 0)
-- Dependencies: 369
-- Name: TABLE account_following_playlist; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.account_following_playlist TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.account_following_playlist TO read_write;


--
-- TOC entry 6495 (class 0 OID 0)
-- Dependencies: 378
-- Name: TABLE account_google_play_purchase; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.account_google_play_purchase TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.account_google_play_purchase TO read_write;


--
-- TOC entry 6497 (class 0 OID 0)
-- Dependencies: 339
-- Name: SEQUENCE account_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.account_id_seq TO read;
GRANT ALL ON SEQUENCE public.account_id_seq TO read_write;


--
-- TOC entry 6498 (class 0 OID 0)
-- Dependencies: 352
-- Name: TABLE account_membership; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.account_membership TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.account_membership TO read_write;


--
-- TOC entry 6500 (class 0 OID 0)
-- Dependencies: 351
-- Name: SEQUENCE account_membership_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.account_membership_id_seq TO read;
GRANT ALL ON SEQUENCE public.account_membership_id_seq TO read_write;


--
-- TOC entry 6501 (class 0 OID 0)
-- Dependencies: 354
-- Name: TABLE account_membership_status; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.account_membership_status TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.account_membership_status TO read_write;


--
-- TOC entry 6503 (class 0 OID 0)
-- Dependencies: 353
-- Name: SEQUENCE account_membership_status_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.account_membership_status_id_seq TO read;
GRANT ALL ON SEQUENCE public.account_membership_status_id_seq TO read_write;


--
-- TOC entry 6504 (class 0 OID 0)
-- Dependencies: 371
-- Name: TABLE account_notification_channel; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.account_notification_channel TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.account_notification_channel TO read_write;


--
-- TOC entry 6505 (class 0 OID 0)
-- Dependencies: 376
-- Name: TABLE account_paypal_order; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.account_paypal_order TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.account_paypal_order TO read_write;


--
-- TOC entry 6506 (class 0 OID 0)
-- Dependencies: 344
-- Name: TABLE account_profile; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.account_profile TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.account_profile TO read_write;


--
-- TOC entry 6508 (class 0 OID 0)
-- Dependencies: 343
-- Name: SEQUENCE account_profile_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.account_profile_id_seq TO read;
GRANT ALL ON SEQUENCE public.account_profile_id_seq TO read_write;


--
-- TOC entry 6509 (class 0 OID 0)
-- Dependencies: 346
-- Name: TABLE account_reset_password; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.account_reset_password TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.account_reset_password TO read_write;


--
-- TOC entry 6511 (class 0 OID 0)
-- Dependencies: 345
-- Name: SEQUENCE account_reset_password_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.account_reset_password_id_seq TO read;
GRANT ALL ON SEQUENCE public.account_reset_password_id_seq TO read_write;


--
-- TOC entry 6512 (class 0 OID 0)
-- Dependencies: 373
-- Name: TABLE account_up_device; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.account_up_device TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.account_up_device TO read_write;


--
-- TOC entry 6514 (class 0 OID 0)
-- Dependencies: 372
-- Name: SEQUENCE account_up_device_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.account_up_device_id_seq TO read;
GRANT ALL ON SEQUENCE public.account_up_device_id_seq TO read_write;


--
-- TOC entry 6515 (class 0 OID 0)
-- Dependencies: 348
-- Name: TABLE account_verification; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.account_verification TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.account_verification TO read_write;


--
-- TOC entry 6517 (class 0 OID 0)
-- Dependencies: 347
-- Name: SEQUENCE account_verification_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.account_verification_id_seq TO read;
GRANT ALL ON SEQUENCE public.account_verification_id_seq TO read_write;


--
-- TOC entry 6518 (class 0 OID 0)
-- Dependencies: 218
-- Name: TABLE category; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.category TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.category TO read_write;


--
-- TOC entry 6520 (class 0 OID 0)
-- Dependencies: 217
-- Name: SEQUENCE category_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.category_id_seq TO read;
GRANT ALL ON SEQUENCE public.category_id_seq TO read_write;


--
-- TOC entry 6521 (class 0 OID 0)
-- Dependencies: 228
-- Name: TABLE channel; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.channel TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.channel TO read_write;


--
-- TOC entry 6522 (class 0 OID 0)
-- Dependencies: 232
-- Name: TABLE channel_about; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.channel_about TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.channel_about TO read_write;


--
-- TOC entry 6524 (class 0 OID 0)
-- Dependencies: 231
-- Name: SEQUENCE channel_about_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.channel_about_id_seq TO read;
GRANT ALL ON SEQUENCE public.channel_about_id_seq TO read_write;


--
-- TOC entry 6525 (class 0 OID 0)
-- Dependencies: 234
-- Name: TABLE channel_category; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.channel_category TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.channel_category TO read_write;


--
-- TOC entry 6527 (class 0 OID 0)
-- Dependencies: 233
-- Name: SEQUENCE channel_category_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.channel_category_id_seq TO read;
GRANT ALL ON SEQUENCE public.channel_category_id_seq TO read_write;


--
-- TOC entry 6528 (class 0 OID 0)
-- Dependencies: 236
-- Name: TABLE channel_chat; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.channel_chat TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.channel_chat TO read_write;


--
-- TOC entry 6530 (class 0 OID 0)
-- Dependencies: 235
-- Name: SEQUENCE channel_chat_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.channel_chat_id_seq TO read;
GRANT ALL ON SEQUENCE public.channel_chat_id_seq TO read_write;


--
-- TOC entry 6531 (class 0 OID 0)
-- Dependencies: 238
-- Name: TABLE channel_description; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.channel_description TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.channel_description TO read_write;


--
-- TOC entry 6533 (class 0 OID 0)
-- Dependencies: 237
-- Name: SEQUENCE channel_description_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.channel_description_id_seq TO read;
GRANT ALL ON SEQUENCE public.channel_description_id_seq TO read_write;


--
-- TOC entry 6534 (class 0 OID 0)
-- Dependencies: 240
-- Name: TABLE channel_funding; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.channel_funding TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.channel_funding TO read_write;


--
-- TOC entry 6536 (class 0 OID 0)
-- Dependencies: 239
-- Name: SEQUENCE channel_funding_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.channel_funding_id_seq TO read;
GRANT ALL ON SEQUENCE public.channel_funding_id_seq TO read_write;


--
-- TOC entry 6538 (class 0 OID 0)
-- Dependencies: 227
-- Name: SEQUENCE channel_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.channel_id_seq TO read;
GRANT ALL ON SEQUENCE public.channel_id_seq TO read_write;


--
-- TOC entry 6539 (class 0 OID 0)
-- Dependencies: 242
-- Name: TABLE channel_image; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.channel_image TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.channel_image TO read_write;


--
-- TOC entry 6541 (class 0 OID 0)
-- Dependencies: 241
-- Name: SEQUENCE channel_image_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.channel_image_id_seq TO read;
GRANT ALL ON SEQUENCE public.channel_image_id_seq TO read_write;


--
-- TOC entry 6542 (class 0 OID 0)
-- Dependencies: 244
-- Name: TABLE channel_internal_settings; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.channel_internal_settings TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.channel_internal_settings TO read_write;


--
-- TOC entry 6544 (class 0 OID 0)
-- Dependencies: 243
-- Name: SEQUENCE channel_internal_settings_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.channel_internal_settings_id_seq TO read;
GRANT ALL ON SEQUENCE public.channel_internal_settings_id_seq TO read_write;


--
-- TOC entry 6545 (class 0 OID 0)
-- Dependencies: 230
-- Name: TABLE channel_itunes_type; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.channel_itunes_type TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.channel_itunes_type TO read_write;


--
-- TOC entry 6547 (class 0 OID 0)
-- Dependencies: 229
-- Name: SEQUENCE channel_itunes_type_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.channel_itunes_type_id_seq TO read;
GRANT ALL ON SEQUENCE public.channel_itunes_type_id_seq TO read_write;


--
-- TOC entry 6548 (class 0 OID 0)
-- Dependencies: 246
-- Name: TABLE channel_license; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.channel_license TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.channel_license TO read_write;


--
-- TOC entry 6550 (class 0 OID 0)
-- Dependencies: 245
-- Name: SEQUENCE channel_license_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.channel_license_id_seq TO read;
GRANT ALL ON SEQUENCE public.channel_license_id_seq TO read_write;


--
-- TOC entry 6551 (class 0 OID 0)
-- Dependencies: 248
-- Name: TABLE channel_location; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.channel_location TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.channel_location TO read_write;


--
-- TOC entry 6553 (class 0 OID 0)
-- Dependencies: 247
-- Name: SEQUENCE channel_location_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.channel_location_id_seq TO read;
GRANT ALL ON SEQUENCE public.channel_location_id_seq TO read_write;


--
-- TOC entry 6554 (class 0 OID 0)
-- Dependencies: 250
-- Name: TABLE channel_person; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.channel_person TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.channel_person TO read_write;


--
-- TOC entry 6556 (class 0 OID 0)
-- Dependencies: 249
-- Name: SEQUENCE channel_person_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.channel_person_id_seq TO read;
GRANT ALL ON SEQUENCE public.channel_person_id_seq TO read_write;


--
-- TOC entry 6557 (class 0 OID 0)
-- Dependencies: 252
-- Name: TABLE channel_podroll; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.channel_podroll TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.channel_podroll TO read_write;


--
-- TOC entry 6559 (class 0 OID 0)
-- Dependencies: 251
-- Name: SEQUENCE channel_podroll_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.channel_podroll_id_seq TO read;
GRANT ALL ON SEQUENCE public.channel_podroll_id_seq TO read_write;


--
-- TOC entry 6560 (class 0 OID 0)
-- Dependencies: 254
-- Name: TABLE channel_podroll_remote_item; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.channel_podroll_remote_item TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.channel_podroll_remote_item TO read_write;


--
-- TOC entry 6562 (class 0 OID 0)
-- Dependencies: 253
-- Name: SEQUENCE channel_podroll_remote_item_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.channel_podroll_remote_item_id_seq TO read;
GRANT ALL ON SEQUENCE public.channel_podroll_remote_item_id_seq TO read_write;


--
-- TOC entry 6563 (class 0 OID 0)
-- Dependencies: 256
-- Name: TABLE channel_publisher; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.channel_publisher TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.channel_publisher TO read_write;


--
-- TOC entry 6565 (class 0 OID 0)
-- Dependencies: 255
-- Name: SEQUENCE channel_publisher_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.channel_publisher_id_seq TO read;
GRANT ALL ON SEQUENCE public.channel_publisher_id_seq TO read_write;


--
-- TOC entry 6566 (class 0 OID 0)
-- Dependencies: 258
-- Name: TABLE channel_publisher_remote_item; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.channel_publisher_remote_item TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.channel_publisher_remote_item TO read_write;


--
-- TOC entry 6568 (class 0 OID 0)
-- Dependencies: 257
-- Name: SEQUENCE channel_publisher_remote_item_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.channel_publisher_remote_item_id_seq TO read;
GRANT ALL ON SEQUENCE public.channel_publisher_remote_item_id_seq TO read_write;


--
-- TOC entry 6569 (class 0 OID 0)
-- Dependencies: 260
-- Name: TABLE channel_remote_item; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.channel_remote_item TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.channel_remote_item TO read_write;


--
-- TOC entry 6571 (class 0 OID 0)
-- Dependencies: 259
-- Name: SEQUENCE channel_remote_item_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.channel_remote_item_id_seq TO read;
GRANT ALL ON SEQUENCE public.channel_remote_item_id_seq TO read_write;


--
-- TOC entry 6572 (class 0 OID 0)
-- Dependencies: 262
-- Name: TABLE channel_season; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.channel_season TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.channel_season TO read_write;


--
-- TOC entry 6574 (class 0 OID 0)
-- Dependencies: 261
-- Name: SEQUENCE channel_season_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.channel_season_id_seq TO read;
GRANT ALL ON SEQUENCE public.channel_season_id_seq TO read_write;


--
-- TOC entry 6575 (class 0 OID 0)
-- Dependencies: 264
-- Name: TABLE channel_social_interact; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.channel_social_interact TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.channel_social_interact TO read_write;


--
-- TOC entry 6577 (class 0 OID 0)
-- Dependencies: 263
-- Name: SEQUENCE channel_social_interact_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.channel_social_interact_id_seq TO read;
GRANT ALL ON SEQUENCE public.channel_social_interact_id_seq TO read_write;


--
-- TOC entry 6578 (class 0 OID 0)
-- Dependencies: 266
-- Name: TABLE channel_trailer; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.channel_trailer TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.channel_trailer TO read_write;


--
-- TOC entry 6580 (class 0 OID 0)
-- Dependencies: 265
-- Name: SEQUENCE channel_trailer_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.channel_trailer_id_seq TO read;
GRANT ALL ON SEQUENCE public.channel_trailer_id_seq TO read_write;


--
-- TOC entry 6581 (class 0 OID 0)
-- Dependencies: 268
-- Name: TABLE channel_txt; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.channel_txt TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.channel_txt TO read_write;


--
-- TOC entry 6583 (class 0 OID 0)
-- Dependencies: 267
-- Name: SEQUENCE channel_txt_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.channel_txt_id_seq TO read;
GRANT ALL ON SEQUENCE public.channel_txt_id_seq TO read_write;


--
-- TOC entry 6584 (class 0 OID 0)
-- Dependencies: 270
-- Name: TABLE channel_value; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.channel_value TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.channel_value TO read_write;


--
-- TOC entry 6586 (class 0 OID 0)
-- Dependencies: 269
-- Name: SEQUENCE channel_value_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.channel_value_id_seq TO read;
GRANT ALL ON SEQUENCE public.channel_value_id_seq TO read_write;


--
-- TOC entry 6587 (class 0 OID 0)
-- Dependencies: 272
-- Name: TABLE channel_value_recipient; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.channel_value_recipient TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.channel_value_recipient TO read_write;


--
-- TOC entry 6589 (class 0 OID 0)
-- Dependencies: 271
-- Name: SEQUENCE channel_value_recipient_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.channel_value_recipient_id_seq TO read;
GRANT ALL ON SEQUENCE public.channel_value_recipient_id_seq TO read_write;


--
-- TOC entry 6590 (class 0 OID 0)
-- Dependencies: 358
-- Name: TABLE clip; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.clip TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.clip TO read_write;


--
-- TOC entry 6592 (class 0 OID 0)
-- Dependencies: 357
-- Name: SEQUENCE clip_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.clip_id_seq TO read;
GRANT ALL ON SEQUENCE public.clip_id_seq TO read_write;


--
-- TOC entry 6593 (class 0 OID 0)
-- Dependencies: 224
-- Name: TABLE feed; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.feed TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.feed TO read_write;


--
-- TOC entry 6594 (class 0 OID 0)
-- Dependencies: 222
-- Name: TABLE feed_flag_status; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.feed_flag_status TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.feed_flag_status TO read_write;


--
-- TOC entry 6596 (class 0 OID 0)
-- Dependencies: 221
-- Name: SEQUENCE feed_flag_status_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.feed_flag_status_id_seq TO read;
GRANT ALL ON SEQUENCE public.feed_flag_status_id_seq TO read_write;


--
-- TOC entry 6598 (class 0 OID 0)
-- Dependencies: 223
-- Name: SEQUENCE feed_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.feed_id_seq TO read;
GRANT ALL ON SEQUENCE public.feed_id_seq TO read_write;


--
-- TOC entry 6599 (class 0 OID 0)
-- Dependencies: 226
-- Name: TABLE feed_log; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.feed_log TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.feed_log TO read_write;


--
-- TOC entry 6601 (class 0 OID 0)
-- Dependencies: 225
-- Name: SEQUENCE feed_log_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.feed_log_id_seq TO read;
GRANT ALL ON SEQUENCE public.feed_log_id_seq TO read_write;


--
-- TOC entry 6602 (class 0 OID 0)
-- Dependencies: 276
-- Name: TABLE item; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item TO read_write;


--
-- TOC entry 6603 (class 0 OID 0)
-- Dependencies: 280
-- Name: TABLE item_about; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_about TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_about TO read_write;


--
-- TOC entry 6605 (class 0 OID 0)
-- Dependencies: 279
-- Name: SEQUENCE item_about_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_about_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_about_id_seq TO read_write;


--
-- TOC entry 6606 (class 0 OID 0)
-- Dependencies: 286
-- Name: TABLE item_chapter; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_chapter TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_chapter TO read_write;


--
-- TOC entry 6608 (class 0 OID 0)
-- Dependencies: 285
-- Name: SEQUENCE item_chapter_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_chapter_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_chapter_id_seq TO read_write;


--
-- TOC entry 6609 (class 0 OID 0)
-- Dependencies: 288
-- Name: TABLE item_chapter_location; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_chapter_location TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_chapter_location TO read_write;


--
-- TOC entry 6611 (class 0 OID 0)
-- Dependencies: 287
-- Name: SEQUENCE item_chapter_location_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_chapter_location_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_chapter_location_id_seq TO read_write;


--
-- TOC entry 6612 (class 0 OID 0)
-- Dependencies: 282
-- Name: TABLE item_chapters_feed; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_chapters_feed TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_chapters_feed TO read_write;


--
-- TOC entry 6614 (class 0 OID 0)
-- Dependencies: 281
-- Name: SEQUENCE item_chapters_feed_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_chapters_feed_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_chapters_feed_id_seq TO read_write;


--
-- TOC entry 6615 (class 0 OID 0)
-- Dependencies: 284
-- Name: TABLE item_chapters_feed_log; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_chapters_feed_log TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_chapters_feed_log TO read_write;


--
-- TOC entry 6617 (class 0 OID 0)
-- Dependencies: 283
-- Name: SEQUENCE item_chapters_feed_log_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_chapters_feed_log_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_chapters_feed_log_id_seq TO read_write;


--
-- TOC entry 6618 (class 0 OID 0)
-- Dependencies: 290
-- Name: TABLE item_chat; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_chat TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_chat TO read_write;


--
-- TOC entry 6620 (class 0 OID 0)
-- Dependencies: 289
-- Name: SEQUENCE item_chat_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_chat_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_chat_id_seq TO read_write;


--
-- TOC entry 6621 (class 0 OID 0)
-- Dependencies: 292
-- Name: TABLE item_content_link; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_content_link TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_content_link TO read_write;


--
-- TOC entry 6623 (class 0 OID 0)
-- Dependencies: 291
-- Name: SEQUENCE item_content_link_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_content_link_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_content_link_id_seq TO read_write;


--
-- TOC entry 6624 (class 0 OID 0)
-- Dependencies: 294
-- Name: TABLE item_description; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_description TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_description TO read_write;


--
-- TOC entry 6626 (class 0 OID 0)
-- Dependencies: 293
-- Name: SEQUENCE item_description_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_description_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_description_id_seq TO read_write;


--
-- TOC entry 6627 (class 0 OID 0)
-- Dependencies: 296
-- Name: TABLE item_enclosure; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_enclosure TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_enclosure TO read_write;


--
-- TOC entry 6629 (class 0 OID 0)
-- Dependencies: 295
-- Name: SEQUENCE item_enclosure_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_enclosure_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_enclosure_id_seq TO read_write;


--
-- TOC entry 6630 (class 0 OID 0)
-- Dependencies: 300
-- Name: TABLE item_enclosure_integrity; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_enclosure_integrity TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_enclosure_integrity TO read_write;


--
-- TOC entry 6632 (class 0 OID 0)
-- Dependencies: 299
-- Name: SEQUENCE item_enclosure_integrity_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_enclosure_integrity_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_enclosure_integrity_id_seq TO read_write;


--
-- TOC entry 6633 (class 0 OID 0)
-- Dependencies: 298
-- Name: TABLE item_enclosure_source; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_enclosure_source TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_enclosure_source TO read_write;


--
-- TOC entry 6635 (class 0 OID 0)
-- Dependencies: 297
-- Name: SEQUENCE item_enclosure_source_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_enclosure_source_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_enclosure_source_id_seq TO read_write;


--
-- TOC entry 6636 (class 0 OID 0)
-- Dependencies: 274
-- Name: TABLE item_flag_status; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_flag_status TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_flag_status TO read_write;


--
-- TOC entry 6638 (class 0 OID 0)
-- Dependencies: 273
-- Name: SEQUENCE item_flag_status_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_flag_status_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_flag_status_id_seq TO read_write;


--
-- TOC entry 6639 (class 0 OID 0)
-- Dependencies: 302
-- Name: TABLE item_funding; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_funding TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_funding TO read_write;


--
-- TOC entry 6641 (class 0 OID 0)
-- Dependencies: 301
-- Name: SEQUENCE item_funding_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_funding_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_funding_id_seq TO read_write;


--
-- TOC entry 6643 (class 0 OID 0)
-- Dependencies: 275
-- Name: SEQUENCE item_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_id_seq TO read_write;


--
-- TOC entry 6644 (class 0 OID 0)
-- Dependencies: 304
-- Name: TABLE item_image; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_image TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_image TO read_write;


--
-- TOC entry 6646 (class 0 OID 0)
-- Dependencies: 303
-- Name: SEQUENCE item_image_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_image_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_image_id_seq TO read_write;


--
-- TOC entry 6647 (class 0 OID 0)
-- Dependencies: 278
-- Name: TABLE item_itunes_episode_type; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_itunes_episode_type TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_itunes_episode_type TO read_write;


--
-- TOC entry 6649 (class 0 OID 0)
-- Dependencies: 277
-- Name: SEQUENCE item_itunes_episode_type_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_itunes_episode_type_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_itunes_episode_type_id_seq TO read_write;


--
-- TOC entry 6650 (class 0 OID 0)
-- Dependencies: 306
-- Name: TABLE item_license; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_license TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_license TO read_write;


--
-- TOC entry 6652 (class 0 OID 0)
-- Dependencies: 305
-- Name: SEQUENCE item_license_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_license_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_license_id_seq TO read_write;


--
-- TOC entry 6653 (class 0 OID 0)
-- Dependencies: 308
-- Name: TABLE item_location; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_location TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_location TO read_write;


--
-- TOC entry 6655 (class 0 OID 0)
-- Dependencies: 307
-- Name: SEQUENCE item_location_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_location_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_location_id_seq TO read_write;


--
-- TOC entry 6656 (class 0 OID 0)
-- Dependencies: 310
-- Name: TABLE item_person; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_person TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_person TO read_write;


--
-- TOC entry 6658 (class 0 OID 0)
-- Dependencies: 309
-- Name: SEQUENCE item_person_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_person_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_person_id_seq TO read_write;


--
-- TOC entry 6659 (class 0 OID 0)
-- Dependencies: 312
-- Name: TABLE item_season; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_season TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_season TO read_write;


--
-- TOC entry 6660 (class 0 OID 0)
-- Dependencies: 314
-- Name: TABLE item_season_episode; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_season_episode TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_season_episode TO read_write;


--
-- TOC entry 6662 (class 0 OID 0)
-- Dependencies: 313
-- Name: SEQUENCE item_season_episode_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_season_episode_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_season_episode_id_seq TO read_write;


--
-- TOC entry 6664 (class 0 OID 0)
-- Dependencies: 311
-- Name: SEQUENCE item_season_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_season_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_season_id_seq TO read_write;


--
-- TOC entry 6665 (class 0 OID 0)
-- Dependencies: 316
-- Name: TABLE item_social_interact; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_social_interact TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_social_interact TO read_write;


--
-- TOC entry 6667 (class 0 OID 0)
-- Dependencies: 315
-- Name: SEQUENCE item_social_interact_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_social_interact_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_social_interact_id_seq TO read_write;


--
-- TOC entry 6668 (class 0 OID 0)
-- Dependencies: 318
-- Name: TABLE item_soundbite; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_soundbite TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_soundbite TO read_write;


--
-- TOC entry 6670 (class 0 OID 0)
-- Dependencies: 317
-- Name: SEQUENCE item_soundbite_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_soundbite_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_soundbite_id_seq TO read_write;


--
-- TOC entry 6671 (class 0 OID 0)
-- Dependencies: 320
-- Name: TABLE item_transcript; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_transcript TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_transcript TO read_write;


--
-- TOC entry 6673 (class 0 OID 0)
-- Dependencies: 319
-- Name: SEQUENCE item_transcript_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_transcript_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_transcript_id_seq TO read_write;


--
-- TOC entry 6674 (class 0 OID 0)
-- Dependencies: 322
-- Name: TABLE item_txt; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_txt TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_txt TO read_write;


--
-- TOC entry 6676 (class 0 OID 0)
-- Dependencies: 321
-- Name: SEQUENCE item_txt_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_txt_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_txt_id_seq TO read_write;


--
-- TOC entry 6677 (class 0 OID 0)
-- Dependencies: 324
-- Name: TABLE item_value; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_value TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_value TO read_write;


--
-- TOC entry 6679 (class 0 OID 0)
-- Dependencies: 323
-- Name: SEQUENCE item_value_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_value_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_value_id_seq TO read_write;


--
-- TOC entry 6680 (class 0 OID 0)
-- Dependencies: 326
-- Name: TABLE item_value_recipient; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_value_recipient TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_value_recipient TO read_write;


--
-- TOC entry 6682 (class 0 OID 0)
-- Dependencies: 325
-- Name: SEQUENCE item_value_recipient_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_value_recipient_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_value_recipient_id_seq TO read_write;


--
-- TOC entry 6683 (class 0 OID 0)
-- Dependencies: 328
-- Name: TABLE item_value_time_split; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_value_time_split TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_value_time_split TO read_write;


--
-- TOC entry 6685 (class 0 OID 0)
-- Dependencies: 327
-- Name: SEQUENCE item_value_time_split_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_value_time_split_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_value_time_split_id_seq TO read_write;


--
-- TOC entry 6686 (class 0 OID 0)
-- Dependencies: 332
-- Name: TABLE item_value_time_split_recipient; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_value_time_split_recipient TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_value_time_split_recipient TO read_write;


--
-- TOC entry 6688 (class 0 OID 0)
-- Dependencies: 331
-- Name: SEQUENCE item_value_time_split_recipient_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_value_time_split_recipient_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_value_time_split_recipient_id_seq TO read_write;


--
-- TOC entry 6689 (class 0 OID 0)
-- Dependencies: 330
-- Name: TABLE item_value_time_split_remote_item; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.item_value_time_split_remote_item TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.item_value_time_split_remote_item TO read_write;


--
-- TOC entry 6691 (class 0 OID 0)
-- Dependencies: 329
-- Name: SEQUENCE item_value_time_split_remote_item_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.item_value_time_split_remote_item_id_seq TO read;
GRANT ALL ON SEQUENCE public.item_value_time_split_remote_item_id_seq TO read_write;


--
-- TOC entry 6692 (class 0 OID 0)
-- Dependencies: 336
-- Name: TABLE live_item; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.live_item TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.live_item TO read_write;


--
-- TOC entry 6694 (class 0 OID 0)
-- Dependencies: 335
-- Name: SEQUENCE live_item_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.live_item_id_seq TO read;
GRANT ALL ON SEQUENCE public.live_item_id_seq TO read_write;


--
-- TOC entry 6695 (class 0 OID 0)
-- Dependencies: 334
-- Name: TABLE live_item_status; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.live_item_status TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.live_item_status TO read_write;


--
-- TOC entry 6697 (class 0 OID 0)
-- Dependencies: 333
-- Name: SEQUENCE live_item_status_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.live_item_status_id_seq TO read;
GRANT ALL ON SEQUENCE public.live_item_status_id_seq TO read_write;


--
-- TOC entry 6698 (class 0 OID 0)
-- Dependencies: 220
-- Name: TABLE medium; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.medium TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.medium TO read_write;


--
-- TOC entry 6700 (class 0 OID 0)
-- Dependencies: 219
-- Name: SEQUENCE medium_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.medium_id_seq TO read;
GRANT ALL ON SEQUENCE public.medium_id_seq TO read_write;


--
-- TOC entry 6701 (class 0 OID 0)
-- Dependencies: 379
-- Name: TABLE membership_claim_token; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.membership_claim_token TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.membership_claim_token TO read_write;


--
-- TOC entry 6702 (class 0 OID 0)
-- Dependencies: 360
-- Name: TABLE playlist; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.playlist TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.playlist TO read_write;


--
-- TOC entry 6704 (class 0 OID 0)
-- Dependencies: 359
-- Name: SEQUENCE playlist_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.playlist_id_seq TO read;
GRANT ALL ON SEQUENCE public.playlist_id_seq TO read_write;


--
-- TOC entry 6705 (class 0 OID 0)
-- Dependencies: 362
-- Name: TABLE playlist_resource; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.playlist_resource TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.playlist_resource TO read_write;


--
-- TOC entry 6707 (class 0 OID 0)
-- Dependencies: 361
-- Name: SEQUENCE playlist_resource_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.playlist_resource_id_seq TO read;
GRANT ALL ON SEQUENCE public.playlist_resource_id_seq TO read_write;


--
-- TOC entry 6708 (class 0 OID 0)
-- Dependencies: 364
-- Name: TABLE queue; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.queue TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.queue TO read_write;


--
-- TOC entry 6710 (class 0 OID 0)
-- Dependencies: 363
-- Name: SEQUENCE queue_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.queue_id_seq TO read;
GRANT ALL ON SEQUENCE public.queue_id_seq TO read_write;


--
-- TOC entry 6711 (class 0 OID 0)
-- Dependencies: 366
-- Name: TABLE queue_resource; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.queue_resource TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.queue_resource TO read_write;


--
-- TOC entry 6713 (class 0 OID 0)
-- Dependencies: 365
-- Name: SEQUENCE queue_resource_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.queue_resource_id_seq TO read;
GRANT ALL ON SEQUENCE public.queue_resource_id_seq TO read_write;


--
-- TOC entry 6714 (class 0 OID 0)
-- Dependencies: 338
-- Name: TABLE sharable_status; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.sharable_status TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.sharable_status TO read_write;


--
-- TOC entry 6716 (class 0 OID 0)
-- Dependencies: 337
-- Name: SEQUENCE sharable_status_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.sharable_status_id_seq TO read;
GRANT ALL ON SEQUENCE public.sharable_status_id_seq TO read_write;


--
-- TOC entry 6717 (class 0 OID 0)
-- Dependencies: 401
-- Name: TABLE stats_aggregated_account; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.stats_aggregated_account TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.stats_aggregated_account TO read_write;


--
-- TOC entry 6719 (class 0 OID 0)
-- Dependencies: 400
-- Name: SEQUENCE stats_aggregated_account_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.stats_aggregated_account_id_seq TO read;
GRANT ALL ON SEQUENCE public.stats_aggregated_account_id_seq TO read_write;


--
-- TOC entry 6720 (class 0 OID 0)
-- Dependencies: 385
-- Name: TABLE stats_aggregated_channel; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.stats_aggregated_channel TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.stats_aggregated_channel TO read_write;


--
-- TOC entry 6722 (class 0 OID 0)
-- Dependencies: 384
-- Name: SEQUENCE stats_aggregated_channel_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.stats_aggregated_channel_id_seq TO read;
GRANT ALL ON SEQUENCE public.stats_aggregated_channel_id_seq TO read_write;


--
-- TOC entry 6723 (class 0 OID 0)
-- Dependencies: 393
-- Name: TABLE stats_aggregated_clip; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.stats_aggregated_clip TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.stats_aggregated_clip TO read_write;


--
-- TOC entry 6725 (class 0 OID 0)
-- Dependencies: 392
-- Name: SEQUENCE stats_aggregated_clip_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.stats_aggregated_clip_id_seq TO read;
GRANT ALL ON SEQUENCE public.stats_aggregated_clip_id_seq TO read_write;


--
-- TOC entry 6726 (class 0 OID 0)
-- Dependencies: 389
-- Name: TABLE stats_aggregated_item; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.stats_aggregated_item TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.stats_aggregated_item TO read_write;


--
-- TOC entry 6728 (class 0 OID 0)
-- Dependencies: 388
-- Name: SEQUENCE stats_aggregated_item_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.stats_aggregated_item_id_seq TO read;
GRANT ALL ON SEQUENCE public.stats_aggregated_item_id_seq TO read_write;


--
-- TOC entry 6729 (class 0 OID 0)
-- Dependencies: 397
-- Name: TABLE stats_aggregated_playlist; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.stats_aggregated_playlist TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.stats_aggregated_playlist TO read_write;


--
-- TOC entry 6731 (class 0 OID 0)
-- Dependencies: 396
-- Name: SEQUENCE stats_aggregated_playlist_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.stats_aggregated_playlist_id_seq TO read;
GRANT ALL ON SEQUENCE public.stats_aggregated_playlist_id_seq TO read_write;


--
-- TOC entry 6732 (class 0 OID 0)
-- Dependencies: 381
-- Name: TABLE stats_track_account_guid; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.stats_track_account_guid TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.stats_track_account_guid TO read_write;


--
-- TOC entry 6734 (class 0 OID 0)
-- Dependencies: 380
-- Name: SEQUENCE stats_track_account_guid_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.stats_track_account_guid_id_seq TO read;
GRANT ALL ON SEQUENCE public.stats_track_account_guid_id_seq TO read_write;


--
-- TOC entry 6735 (class 0 OID 0)
-- Dependencies: 399
-- Name: TABLE stats_track_event_account; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.stats_track_event_account TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.stats_track_event_account TO read_write;


--
-- TOC entry 6737 (class 0 OID 0)
-- Dependencies: 398
-- Name: SEQUENCE stats_track_event_account_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.stats_track_event_account_id_seq TO read;
GRANT ALL ON SEQUENCE public.stats_track_event_account_id_seq TO read_write;


--
-- TOC entry 6738 (class 0 OID 0)
-- Dependencies: 383
-- Name: TABLE stats_track_event_channel; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.stats_track_event_channel TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.stats_track_event_channel TO read_write;


--
-- TOC entry 6740 (class 0 OID 0)
-- Dependencies: 382
-- Name: SEQUENCE stats_track_event_channel_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.stats_track_event_channel_id_seq TO read;
GRANT ALL ON SEQUENCE public.stats_track_event_channel_id_seq TO read_write;


--
-- TOC entry 6741 (class 0 OID 0)
-- Dependencies: 391
-- Name: TABLE stats_track_event_clip; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.stats_track_event_clip TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.stats_track_event_clip TO read_write;


--
-- TOC entry 6743 (class 0 OID 0)
-- Dependencies: 390
-- Name: SEQUENCE stats_track_event_clip_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.stats_track_event_clip_id_seq TO read;
GRANT ALL ON SEQUENCE public.stats_track_event_clip_id_seq TO read_write;


--
-- TOC entry 6744 (class 0 OID 0)
-- Dependencies: 387
-- Name: TABLE stats_track_event_item; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.stats_track_event_item TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.stats_track_event_item TO read_write;


--
-- TOC entry 6746 (class 0 OID 0)
-- Dependencies: 386
-- Name: SEQUENCE stats_track_event_item_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.stats_track_event_item_id_seq TO read;
GRANT ALL ON SEQUENCE public.stats_track_event_item_id_seq TO read_write;


--
-- TOC entry 6747 (class 0 OID 0)
-- Dependencies: 395
-- Name: TABLE stats_track_event_playlist; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.stats_track_event_playlist TO read;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.stats_track_event_playlist TO read_write;


--
-- TOC entry 6749 (class 0 OID 0)
-- Dependencies: 394
-- Name: SEQUENCE stats_track_event_playlist_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON SEQUENCE public.stats_track_event_playlist_id_seq TO read;
GRANT ALL ON SEQUENCE public.stats_track_event_playlist_id_seq TO read_write;


--
-- TOC entry 2574 (class 826 OID 24808)
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT SELECT ON SEQUENCES TO read;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON SEQUENCES TO read_write;


--
-- TOC entry 2573 (class 826 OID 24807)
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT SELECT ON TABLES TO read;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT SELECT,INSERT,DELETE,UPDATE ON TABLES TO read_write;


-- Completed on 2025-06-04 18:24:09

--
-- PostgreSQL database dump complete
--

