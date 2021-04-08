--
-- PostgreSQL database dump
--

-- Dumped from database version 12.5 (Ubuntu 12.5-1.pgdg16.04+1)
-- Dumped by pg_dump version 13.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: pg_trgm; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA public;


--
-- Name: EXTENSION pg_trgm; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pg_trgm IS 'text similarity measurement and index searching based on trigrams';


--
-- Name: unaccent; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS unaccent WITH SCHEMA public;


--
-- Name: EXTENSION unaccent; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION unaccent IS 'text search dictionary that removes accents';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: kvdomingo
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO kvdomingo;

--
-- Name: alias; Type: TABLE; Schema: public; Owner: kvdomingo
--

CREATE TABLE public.alias (
    id integer NOT NULL,
    alias character varying(64),
    member_id integer
);


ALTER TABLE public.alias OWNER TO kvdomingo;

--
-- Name: alias_id_seq; Type: SEQUENCE; Schema: public; Owner: kvdomingo
--

CREATE SEQUENCE public.alias_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.alias_id_seq OWNER TO kvdomingo;

--
-- Name: alias_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kvdomingo
--

ALTER SEQUENCE public.alias_id_seq OWNED BY public.alias.id;


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: kvdomingo
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO kvdomingo;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: kvdomingo
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO kvdomingo;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kvdomingo
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: kvdomingo
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO kvdomingo;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: kvdomingo
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO kvdomingo;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kvdomingo
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: kvdomingo
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO kvdomingo;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: kvdomingo
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO kvdomingo;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kvdomingo
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: kvdomingo
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO kvdomingo;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: kvdomingo
--

CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO kvdomingo;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: kvdomingo
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO kvdomingo;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kvdomingo
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: kvdomingo
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO kvdomingo;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kvdomingo
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: kvdomingo
--

CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO kvdomingo;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: kvdomingo
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO kvdomingo;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kvdomingo
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: bot_group; Type: TABLE; Schema: public; Owner: kvdomingo
--

CREATE TABLE public.bot_group (
    id integer NOT NULL,
    name character varying(32) NOT NULL,
    vlive_channel_code character varying(32),
    vlive_channel_seq bigint,
    vlive_last_seq bigint,
    twitter_user_name character varying(16) NOT NULL,
    instagram_user_name character varying(32) NOT NULL
);


ALTER TABLE public.bot_group OWNER TO kvdomingo;

--
-- Name: bot_group_id_seq; Type: SEQUENCE; Schema: public; Owner: kvdomingo
--

CREATE SEQUENCE public.bot_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.bot_group_id_seq OWNER TO kvdomingo;

--
-- Name: bot_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kvdomingo
--

ALTER SEQUENCE public.bot_group_id_seq OWNED BY public.bot_group.id;


--
-- Name: bot_groupalias; Type: TABLE; Schema: public; Owner: kvdomingo
--

CREATE TABLE public.bot_groupalias (
    id integer NOT NULL,
    alias character varying(16) NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.bot_groupalias OWNER TO kvdomingo;

--
-- Name: bot_groupalias_id_seq; Type: SEQUENCE; Schema: public; Owner: kvdomingo
--

CREATE SEQUENCE public.bot_groupalias_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.bot_groupalias_id_seq OWNER TO kvdomingo;

--
-- Name: bot_groupalias_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kvdomingo
--

ALTER SEQUENCE public.bot_groupalias_id_seq OWNED BY public.bot_groupalias.id;


--
-- Name: bot_member; Type: TABLE; Schema: public; Owner: kvdomingo
--

CREATE TABLE public.bot_member (
    id integer NOT NULL,
    stage_name character varying(16) NOT NULL,
    given_name character varying(16) NOT NULL,
    family_name character varying(16) NOT NULL,
    english_name character varying(32),
    birthday date,
    group_id integer NOT NULL
);


ALTER TABLE public.bot_member OWNER TO kvdomingo;

--
-- Name: bot_member_id_seq; Type: SEQUENCE; Schema: public; Owner: kvdomingo
--

CREATE SEQUENCE public.bot_member_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.bot_member_id_seq OWNER TO kvdomingo;

--
-- Name: bot_member_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kvdomingo
--

ALTER SEQUENCE public.bot_member_id_seq OWNED BY public.bot_member.id;


--
-- Name: bot_memberalias; Type: TABLE; Schema: public; Owner: kvdomingo
--

CREATE TABLE public.bot_memberalias (
    id integer NOT NULL,
    alias character varying(32) NOT NULL,
    member_id integer NOT NULL
);


ALTER TABLE public.bot_memberalias OWNER TO kvdomingo;

--
-- Name: bot_memberalias_id_seq; Type: SEQUENCE; Schema: public; Owner: kvdomingo
--

CREATE SEQUENCE public.bot_memberalias_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.bot_memberalias_id_seq OWNER TO kvdomingo;

--
-- Name: bot_memberalias_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kvdomingo
--

ALTER SEQUENCE public.bot_memberalias_id_seq OWNED BY public.bot_memberalias.id;


--
-- Name: bot_twittermediasource; Type: TABLE; Schema: public; Owner: kvdomingo
--

CREATE TABLE public.bot_twittermediasource (
    id integer NOT NULL,
    account_name character varying(16) NOT NULL,
    member_id integer NOT NULL,
    last_tweet_id bigint
);


ALTER TABLE public.bot_twittermediasource OWNER TO kvdomingo;

--
-- Name: bot_twittermediasource_id_seq; Type: SEQUENCE; Schema: public; Owner: kvdomingo
--

CREATE SEQUENCE public.bot_twittermediasource_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.bot_twittermediasource_id_seq OWNER TO kvdomingo;

--
-- Name: bot_twittermediasource_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kvdomingo
--

ALTER SEQUENCE public.bot_twittermediasource_id_seq OWNED BY public.bot_twittermediasource.id;


--
-- Name: bot_twittermediasubscribedchannel; Type: TABLE; Schema: public; Owner: kvdomingo
--

CREATE TABLE public.bot_twittermediasubscribedchannel (
    id integer NOT NULL,
    channel_id bigint NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.bot_twittermediasubscribedchannel OWNER TO kvdomingo;

--
-- Name: bot_twittermediasubscribedchannel_id_seq; Type: SEQUENCE; Schema: public; Owner: kvdomingo
--

CREATE SEQUENCE public.bot_twittermediasubscribedchannel_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.bot_twittermediasubscribedchannel_id_seq OWNER TO kvdomingo;

--
-- Name: bot_twittermediasubscribedchannel_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kvdomingo
--

ALTER SEQUENCE public.bot_twittermediasubscribedchannel_id_seq OWNED BY public.bot_twittermediasubscribedchannel.id;


--
-- Name: bot_vlivesubscribedchannel; Type: TABLE; Schema: public; Owner: kvdomingo
--

CREATE TABLE public.bot_vlivesubscribedchannel (
    id integer NOT NULL,
    channel_id bigint NOT NULL,
    group_id integer NOT NULL,
    dev_channel boolean NOT NULL
);


ALTER TABLE public.bot_vlivesubscribedchannel OWNER TO kvdomingo;

--
-- Name: bot_vlivesubscribedchannel_id_seq; Type: SEQUENCE; Schema: public; Owner: kvdomingo
--

CREATE SEQUENCE public.bot_vlivesubscribedchannel_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.bot_vlivesubscribedchannel_id_seq OWNER TO kvdomingo;

--
-- Name: bot_vlivesubscribedchannel_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kvdomingo
--

ALTER SEQUENCE public.bot_vlivesubscribedchannel_id_seq OWNED BY public.bot_vlivesubscribedchannel.id;


--
-- Name: twitterchannel; Type: TABLE; Schema: public; Owner: kvdomingo
--

CREATE TABLE public.twitterchannel (
    id integer NOT NULL,
    channel_id bigint,
    group_id integer
);


ALTER TABLE public.twitterchannel OWNER TO kvdomingo;

--
-- Name: channel_id_seq; Type: SEQUENCE; Schema: public; Owner: kvdomingo
--

CREATE SEQUENCE public.channel_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.channel_id_seq OWNER TO kvdomingo;

--
-- Name: channel_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kvdomingo
--

ALTER SEQUENCE public.channel_id_seq OWNED BY public.twitterchannel.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: kvdomingo
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO kvdomingo;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: kvdomingo
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO kvdomingo;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kvdomingo
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: kvdomingo
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO kvdomingo;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: kvdomingo
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO kvdomingo;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kvdomingo
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: kvdomingo
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO kvdomingo;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: kvdomingo
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO kvdomingo;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kvdomingo
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: kvdomingo
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO kvdomingo;

--
-- Name: group; Type: TABLE; Schema: public; Owner: kvdomingo
--

CREATE TABLE public."group" (
    id integer NOT NULL,
    name character varying(64),
    vlive_channel_code character varying(255),
    vlive_channel_seq bigint,
    vlive_last_seq bigint
);


ALTER TABLE public."group" OWNER TO kvdomingo;

--
-- Name: group_id_seq; Type: SEQUENCE; Schema: public; Owner: kvdomingo
--

CREATE SEQUENCE public.group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.group_id_seq OWNER TO kvdomingo;

--
-- Name: group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kvdomingo
--

ALTER SEQUENCE public.group_id_seq OWNED BY public."group".id;


--
-- Name: member; Type: TABLE; Schema: public; Owner: kvdomingo
--

CREATE TABLE public.member (
    id integer NOT NULL,
    stage_name character varying(64),
    given_name character varying(64),
    family_name character varying(64),
    group_id integer,
    birthday date
);


ALTER TABLE public.member OWNER TO kvdomingo;

--
-- Name: member_id_seq; Type: SEQUENCE; Schema: public; Owner: kvdomingo
--

CREATE SEQUENCE public.member_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.member_id_seq OWNER TO kvdomingo;

--
-- Name: member_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kvdomingo
--

ALTER SEQUENCE public.member_id_seq OWNED BY public.member.id;


--
-- Name: twitteraccount; Type: TABLE; Schema: public; Owner: kvdomingo
--

CREATE TABLE public.twitteraccount (
    id integer NOT NULL,
    account_name character varying(255),
    member_id integer,
    last_tweet_id bigint
);


ALTER TABLE public.twitteraccount OWNER TO kvdomingo;

--
-- Name: twitteraccount_id_seq; Type: SEQUENCE; Schema: public; Owner: kvdomingo
--

CREATE SEQUENCE public.twitteraccount_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.twitteraccount_id_seq OWNER TO kvdomingo;

--
-- Name: twitteraccount_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kvdomingo
--

ALTER SEQUENCE public.twitteraccount_id_seq OWNED BY public.twitteraccount.id;


--
-- Name: vlivechannel; Type: TABLE; Schema: public; Owner: kvdomingo
--

CREATE TABLE public.vlivechannel (
    id integer NOT NULL,
    channel_id bigint,
    group_id integer
);


ALTER TABLE public.vlivechannel OWNER TO kvdomingo;

--
-- Name: vlivechannel_id_seq; Type: SEQUENCE; Schema: public; Owner: kvdomingo
--

CREATE SEQUENCE public.vlivechannel_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.vlivechannel_id_seq OWNER TO kvdomingo;

--
-- Name: vlivechannel_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: kvdomingo
--

ALTER SEQUENCE public.vlivechannel_id_seq OWNED BY public.vlivechannel.id;


--
-- Name: alias id; Type: DEFAULT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.alias ALTER COLUMN id SET DEFAULT nextval('public.alias_id_seq'::regclass);


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: bot_group id; Type: DEFAULT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.bot_group ALTER COLUMN id SET DEFAULT nextval('public.bot_group_id_seq'::regclass);


--
-- Name: bot_groupalias id; Type: DEFAULT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.bot_groupalias ALTER COLUMN id SET DEFAULT nextval('public.bot_groupalias_id_seq'::regclass);


--
-- Name: bot_member id; Type: DEFAULT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.bot_member ALTER COLUMN id SET DEFAULT nextval('public.bot_member_id_seq'::regclass);


--
-- Name: bot_memberalias id; Type: DEFAULT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.bot_memberalias ALTER COLUMN id SET DEFAULT nextval('public.bot_memberalias_id_seq'::regclass);


--
-- Name: bot_twittermediasource id; Type: DEFAULT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.bot_twittermediasource ALTER COLUMN id SET DEFAULT nextval('public.bot_twittermediasource_id_seq'::regclass);


--
-- Name: bot_twittermediasubscribedchannel id; Type: DEFAULT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.bot_twittermediasubscribedchannel ALTER COLUMN id SET DEFAULT nextval('public.bot_twittermediasubscribedchannel_id_seq'::regclass);


--
-- Name: bot_vlivesubscribedchannel id; Type: DEFAULT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.bot_vlivesubscribedchannel ALTER COLUMN id SET DEFAULT nextval('public.bot_vlivesubscribedchannel_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: group id; Type: DEFAULT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public."group" ALTER COLUMN id SET DEFAULT nextval('public.group_id_seq'::regclass);


--
-- Name: member id; Type: DEFAULT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.member ALTER COLUMN id SET DEFAULT nextval('public.member_id_seq'::regclass);


--
-- Name: twitteraccount id; Type: DEFAULT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.twitteraccount ALTER COLUMN id SET DEFAULT nextval('public.twitteraccount_id_seq'::regclass);


--
-- Name: twitterchannel id; Type: DEFAULT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.twitterchannel ALTER COLUMN id SET DEFAULT nextval('public.channel_id_seq'::regclass);


--
-- Name: vlivechannel id; Type: DEFAULT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.vlivechannel ALTER COLUMN id SET DEFAULT nextval('public.vlivechannel_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: kvdomingo
--

COPY public.alembic_version (version_num) FROM stdin;
9aa10724f582
\.


--
-- Data for Name: alias; Type: TABLE DATA; Schema: public; Owner: kvdomingo
--

COPY public.alias (id, alias, member_id) FROM stdin;
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: kvdomingo
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: kvdomingo
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: kvdomingo
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add group	1	add_group
2	Can change group	1	change_group
3	Can delete group	1	delete_group
4	Can view group	1	view_group
5	Can add member	2	add_member
6	Can change member	2	change_member
7	Can delete member	2	delete_member
8	Can view member	2	view_member
9	Can add vlive subscribed channel	3	add_vlivesubscribedchannel
10	Can change vlive subscribed channel	3	change_vlivesubscribedchannel
11	Can delete vlive subscribed channel	3	delete_vlivesubscribedchannel
12	Can view vlive subscribed channel	3	view_vlivesubscribedchannel
13	Can add twitter media subscribed channel	4	add_twittermediasubscribedchannel
14	Can change twitter media subscribed channel	4	change_twittermediasubscribedchannel
15	Can delete twitter media subscribed channel	4	delete_twittermediasubscribedchannel
16	Can view twitter media subscribed channel	4	view_twittermediasubscribedchannel
17	Can add twitter media source	5	add_twittermediasource
18	Can change twitter media source	5	change_twittermediasource
19	Can delete twitter media source	5	delete_twittermediasource
20	Can view twitter media source	5	view_twittermediasource
21	Can add member alias	6	add_memberalias
22	Can change member alias	6	change_memberalias
23	Can delete member alias	6	delete_memberalias
24	Can view member alias	6	view_memberalias
25	Can add group alias	7	add_groupalias
26	Can change group alias	7	change_groupalias
27	Can delete group alias	7	delete_groupalias
28	Can view group alias	7	view_groupalias
29	Can add log entry	8	add_logentry
30	Can change log entry	8	change_logentry
31	Can delete log entry	8	delete_logentry
32	Can view log entry	8	view_logentry
33	Can add permission	9	add_permission
34	Can change permission	9	change_permission
35	Can delete permission	9	delete_permission
36	Can view permission	9	view_permission
37	Can add group	10	add_group
38	Can change group	10	change_group
39	Can delete group	10	delete_group
40	Can view group	10	view_group
41	Can add user	11	add_user
42	Can change user	11	change_user
43	Can delete user	11	delete_user
44	Can view user	11	view_user
45	Can add content type	12	add_contenttype
46	Can change content type	12	change_contenttype
47	Can delete content type	12	delete_contenttype
48	Can view content type	12	view_contenttype
49	Can add session	13	add_session
50	Can change session	13	change_session
51	Can delete session	13	delete_session
52	Can view session	13	view_session
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: kvdomingo
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$216000$vos78CNSi2V6$BQicVAhV9cel2KqtaRhJuhyNhAZitZ8YwJvikfy2HTE=	2021-01-25 14:46:07.498842+00	t	kvdomingo			kvdomingo@up.edu.ph	t	t	2020-12-25 14:37:30.549+00
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: kvdomingo
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: kvdomingo
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: bot_group; Type: TABLE DATA; Schema: public; Owner: kvdomingo
--

COPY public.bot_group (id, name, vlive_channel_code, vlive_channel_seq, vlive_last_seq, twitter_user_name, instagram_user_name) FROM stdin;
8	Somi	B4595B	1198	220909		
9	æspa	97CCED	\N	\N		
10	EXO	F94BD	\N	\N		
11	Dreamcatcher	E8D2CB	\N	\N		
12	CLC	F2E189	\N	\N		
13	Chungha	E3437D	\N	\N		
14	IZ*ONE	C1B7AF	\N	\N		
15	(G)I-DLE	CE2621	\N	\N		
16	LOOΠΔ	E1F3A7	\N	\N		
17	SHINee	96DD0B	\N	\N		
6	BTS	FE619	13	238983		
7	MAMAMOO	FCD4B	38	239397		
1	ITZY	BAE889	1093	239459		
3	TWICE	EDBF	6	239569	JYPETWICE	
5	IU	FA895	75	237907		
4	Red Velvet	DCF447	548	236560		
2	BLACKPINK	F001E5	243	236592		
\.


--
-- Data for Name: bot_groupalias; Type: TABLE DATA; Schema: public; Owner: kvdomingo
--

COPY public.bot_groupalias (id, alias, group_id) FROM stdin;
1	itz	1
2	rv	4
3	mink	2
4	more	3
5	tdoong	3
6	red-velvet	4
7	red_velvet	4
8	æ	9
9	insomnia	11
10	redvelvet	4
11	teudoong	3
12	bangtan	6
13	sonyeondan	6
14	bangtan boys	6
15	izone	14
16	gidle	15
17	loona	16
18	idalwi sonyeo	16
19	aespa	9
20	트와이스	3
\.


--
-- Data for Name: bot_member; Type: TABLE DATA; Schema: public; Owner: kvdomingo
--

COPY public.bot_member (id, stage_name, given_name, family_name, english_name, birthday, group_id) FROM stdin;
1	Ryujin	Ryujin	Shin	Joanne	2001-04-17	1
2	Yuna	Yuna	Shin	Hussey	2003-12-09	1
3	Yeji	Yeji	Hwang	Lucy	2000-05-26	1
4	Lia	Jisu	Choi	Julia	2000-07-21	1
5	Chaeryeong	Chaeryeong	Lee	Judy	2001-06-05	1
6	Jennie	Jennie Ruby Jane	Kim	\N	1996-01-16	2
7	Jisoo	Jisoo	Kim	\N	1995-01-03	2
8	Rosé	Chaeyoung	Park	\N	1997-02-11	2
9	Lisa	Pranpriya	Manoban	Lalisa	1997-03-27	2
10	Nayeon	Nayeon	Im	\N	1995-09-22	3
11	Jeongyeon	Jeongyeon	Yoo	\N	1996-11-01	3
12	Momo	Momo	Hirai	\N	1996-11-09	3
13	Sana	Sana	Minatozaki	\N	1996-12-29	3
14	Jihyo	Jisoo	Park	\N	1997-02-01	3
15	Mina	Minari	Myoui	\N	1997-03-24	3
16	Dahyun	Dahyun	Kim	\N	1998-05-28	3
17	Chaeyoung	Chaeyoung	Son	\N	1999-04-23	3
18	Tzuyu	Tzuyu	Chou	\N	1999-06-14	3
19	Irene	Joohyun	Bae	\N	1991-03-29	4
20	Seulgi	Seulgi	Kang	\N	1994-02-10	4
21	Wendy	Seungwan	Shon	\N	1994-02-21	4
22	Joy	Sooyoung	Park	\N	1996-09-03	4
23	Yeri	Yerim	Kim	\N	1999-03-05	4
24	IU	Jieun	Lee	\N	1993-05-16	5
25	Jin	Seokjin	Kim	\N	1992-12-04	6
26	Suga	Yoongi	Min	\N	1993-03-09	6
27	J-Hope	Hoseok	Jung	\N	1994-02-18	6
28	RM	Namjoon	Kim	\N	1994-09-12	6
29	Jimin	Jimin	Park	\N	1995-10-13	6
30	V	Taehyung	Kim	\N	1995-12-30	6
31	Jungkook	Jungkook	Jeon	\N	1997-09-01	6
32	Solar	Yongsun	Kim	\N	1991-02-21	7
33	Moonbyul	Byulyi	Moon	\N	1992-12-22	7
34	Wheein	Wheein	Jung	\N	1995-04-17	7
35	Hwasa	Hyejin	Ahn	\N	1995-07-23	7
36	Somi	Somi	Jeon	Ennik Somi Douma	2001-03-09	8
37	Karina	Jimin	Yoo	\N	2000-04-11	9
38	Giselle	Aeri	Uchinaga	\N	2000-10-30	9
39	Winter	Minjeong	Kim	\N	2001-01-01	9
40	Ningning	Yizhuo	Ning	\N	2002-10-23	9
41	Xiumin	Minseok	Kim	Jin Min Shuo	1990-03-26	10
42	Suho	Junmyeon	Kim	Jin Jun Mian	1991-05-22	10
43	Lay	Jiashuai	Zhang	Zhang Yixing	1991-10-07	10
44	Baekhyun	Baekhyun	Byun	Bian Buo Xian	1992-05-06	10
45	Chen	Jongdae	Kim	Jin Zhong Da	1991-09-21	10
46	Chanyeol	Chanyeol	Park	Piao Can Lie	1992-11-27	10
47	D.O.	Kyungsoo	Doh	Du Qing Zhu	1993-01-12	10
48	Kai	Jongin	Kim	Jin Zhong Ren	1994-01-14	10
49	Sehun	Sehun	Oh	Wu Shi Xun	1994-04-12	10
50	Luhan	Han	Lu	\N	1990-04-20	10
51	Kris	Yifan	Wu	Li Jiaheng	1990-11-06	10
52	Tao	Zitao	Huang	\N	1993-05-02	10
53	JiU	Minji	Kim	Lily	1994-05-17	11
54	SuA	Bora	Kim	Alice	1994-08-10	11
55	Siyeon	Siyeon	Lee	Monica	1995-10-01	11
56	Handong	Dong	Han	Della	1996-03-26	11
57	Yoohyeon	Yoohyeon	Kim	Rachel	1997-01-07	11
58	Dami	Yubin	Lee	Emma	1997-03-07	11
59	Gahyeon	Gahyeon	Lee	Lucy	1999-02-03	11
60	Seungyeon	Seungyeon	Chang	\N	1996-11-06	12
61	Seunghee	Seunghee	Oh	\N	1995-10-05	12
62	Yujin	Yujin	Choi	\N	1996-08-12	12
63	Sorn	Chonnasorn	Sajakul	Kim Soeun	1996-11-18	12
64	Yeeun	Yeeun	Jang	\N	1998-08-10	12
65	Eunbin	Eunbin	Kwon	\N	2000-01-06	12
66	Elkie	Tingyan	Chong	Jang Jungheun	1998-11-02	12
67	Chungha	Chanmi	Kim	\N	1996-02-09	13
68	Eunbi	Eunbi	Kwon	Quan En Fei	1995-09-27	14
69	Sakura	Sakura	Miyawaki	\N	1998-03-19	14
70	Hyewon	Hyewon	Kang	Jiang Huiyun	1999-07-05	14
71	Yena	Yena	Choi	Cui Rui Na	1999-09-29	14
72	Chaeyeon	Chaeyeon	Lee	Li Cai Yan	2000-01-11	14
73	Chaewon	Chaewon	Kim	Jin Cui Yuan	2000-08-01	14
74	Minju	Minju	Kim	Jin Wen Zhou	2001-02-05	14
75	Nako	Nako	Yabuki	\N	2001-06-18	14
76	Hitomi	Hitomi	Honda	\N	2001-10-06	14
77	Yuri	Yuri	Jo	\N	2001-10-22	14
78	Yujin	Yujin	An	An Yu Zhen	2003-09-01	14
79	Wonyoung	Wonyoung	Jang	Zhang Yuan Ying	2004-08-31	14
80	Soyeon	Soyeon	Jeon	\N	1998-08-26	15
81	Miyeon	Miyeon	Cho	\N	1997-01-31	15
82	Minnie	Nicha	Yontararak	Kim Minhee	1997-10-23	15
83	Soojin	Sujin	Seo	\N	1998-03-09	15
84	Yuqi	Woogi	Song	\N	1999-09-23	15
85	Shuhua	Shuhua	Yeh	Yoo Shuhua	2000-01-06	15
86	Haseul	Haseul	Jo	\N	1997-08-18	16
87	Vivi	Gaahei	Wong	Vivian Wong	1996-12-09	16
88	Yves	Sooyoung	Ha	\N	1997-05-24	16
89	Jinsoul	Jinsol	Jung	\N	1997-06-13	16
90	Kim Lip	Jungeun	Kim	\N	1999-02-10	16
91	Chuu	Jiwoo	Kim	\N	1999-10-20	16
92	Heejin	Heejin	Jeon	\N	2000-10-19	16
93	Hyunjin	Hyunjin	Kim	\N	2000-11-15	16
94	Go Won	Chaewon	Park	\N	2000-11-19	16
95	Choerry	Yerim	Choi	\N	2001-06-04	16
96	Olivia Hye	Hyejoo	Son	\N	2001-11-13	16
97	Yeojin	Yeojin	Im	\N	2002-11-11	16
98	Onew	Jinki	Lee	\N	1989-12-14	17
99	Key	Kibum	Kim	\N	1991-09-23	17
100	Minho	Minho	Choi	\N	1991-12-09	17
101	Taemin	Taemin	Lee	\N	1993-07-18	17
102	Jonghyun	Jonghyun	Kim	\N	1990-04-08	17
\.


--
-- Data for Name: bot_memberalias; Type: TABLE DATA; Schema: public; Owner: kvdomingo
--

COPY public.bot_memberalias (id, alias, member_id) FROM stdin;
1	joanne	1
2	julia	4
3	hussey	2
4	lucy	3
5	judy	5
7	chaeng	8
8	roseanne	8
9	pranpriya	9
11	jisoo	4
12	seyoung	17
13	chiyong	17
14	siyong	17
15	maknae	2
16	maknÃ¦	2
18	jisu	4
20	gentle monster	6
21	sooya	7
22	nabong	10
23	dance machine	12
24	gae	13
25	gummy	15
26	myoi	15
27	dubu	16
28	chaeng	17
29	maknae	18
30	maknÃ¦	18
31	chewy	18
32	bÃ¦	19
33	original	19
34	visual	19
35	orihinal	19
36	biswal	19
37	son	21
38	maknae	23
39	maknÃ¦	23
40	rosie	8
41	ros	8
42	jhope	27
43	maknae	31
44	ysl	8
45	turtle	7
46	rabbit	7
47	agust	26
48	maknæ	31
49	monster	28
50	maknæ	31
51	maknæ	2
52	DO	47
53	center	1
54	SRABU	1
55	salamat	1
56	seyoung	17
57	chiyong	17
58	siyong	17
59	maknae	59
\.


--
-- Data for Name: bot_twittermediasource; Type: TABLE DATA; Schema: public; Owner: kvdomingo
--

COPY public.bot_twittermediasource (id, account_name, member_id, last_tweet_id) FROM stdin;
1	ryujinpics	1	\N
2	shinryujinpic	1	\N
3	hourlyryu	1	\N
4	hourlylia	4	\N
5	liarchive	4	\N
6	yunaspics	2	\N
7	yunasarchive	2	\N
8	picyuna	2	\N
9	littIeyuna	2	\N
10	hourlyyeji	3	\N
11	yejigallery	3	\N
12	yejiarchives	3	\N
13	chaerpics	5	\N
14	jenniesarchive	6	\N
15	jenniexpics	6	\N
16	kimjenniepics	6	\N
17	archivejisoo	7	\N
18	jisoosjpg	7	\N
19	jisooarchives	7	\N
20	milkylisapics	9	\N
21	lisapics_	9	\N
22	BLACKPINK_LISA	9	\N
23	archivesrosie	8	\N
24	roseyarchive	8	\N
25	rosesarchive	8	\N
26	nayeonpics	10	\N
27	imnayeonarchive	10	\N
28	archivenayeon	10	\N
29	nayeonarchives	10	\N
30	myjeongarchives	11	\N
31	1101_yjy	11	\N
32	TWICE_JYY	11	\N
33	yjyworld	11	\N
34	dailyhiraimomo	12	\N
35	hiraimomopics	12	\N
36	momosarchives	12	\N
37	hiraidotjpg	12	\N
38	sanapics	13	\N
39	sanaarchive	13	\N
40	sanaspics	13	\N
41	sanarchives	13	\N
42	jihyopictures	14	\N
43	jihyosarchive	14	\N
44	loopjihyo	14	\N
45	jihyospic	14	\N
46	minapics	15	\N
47	archivemina	15	\N
48	minajpgs	15	\N
50	dubupics	16	\N
51	dahyunniepics	16	\N
52	loopsdubu	16	\N
53	bestofdahyun	16	\N
54	chaeyoungpic	17	\N
55	chaeypics	17	\N
56	loopschaeng	17	\N
57	chaengspic	17	\N
58	tzuyudotjpg	18	\N
59	ctzuyupics	18	\N
60	tzuyu	18	\N
61	tzuyuzones	18	\N
62	archivedirene	19	\N
63	picsofirene	19	\N
64	picsofjoo	19	\N
65	bjharchives	19	\N
66	seulgiphotos	20	\N
67	seulpics	20	\N
68	seulgiarchives	20	\N
69	seulgipicts	20	\N
70	archivedwendy	21	\N
71	sonseungwanpics	21	\N
72	wendygallery	21	\N
73	wenpics	21	\N
74	joyjpgs	22	\N
75	picsofsooyoung	22	\N
76	joypics	22	\N
77	joysooyoungpics	22	\N
78	yeripics	23	\N
79	cuteyeripics	23	\N
80	picsofyeri	23	\N
81	archivedyeri	23	\N
82	jieunphotos	24	\N
84	iusarchive	24	\N
85	jieunpic	24	\N
86	iu_archive	24	\N
87	seokjinpicss	25	\N
88	jingallery	25	\N
89	jinspicture	25	\N
90	sugapics	26	\N
91	sugapicshd	26	\N
92	suga_pics	26	\N
93	archivehoseok	27	\N
94	jhopepics	27	\N
95	hopepics	27	\N
96	rmpics4	28	\N
97	rmpics_94	28	\N
98	namupic	28	\N
99	parkjiminpics	29	\N
100	jamjampics	29	\N
101	jiminpics	29	\N
102	kimvpics	30	\N
103	_vantae_k	30	\N
104	taehypic	30	\N
105	kookpiics	31	\N
106	kookpics	31	\N
107	archiveskook	31	\N
108	archiveryujin	1	\N
109	ryujinthings	1	\N
110	ryujinsarchives	1	\N
111	ryudetail	1	\N
112	kimyongsunpics	32	\N
113	solarpics	32	\N
114	yongsunarchive	32	\N
115	filesmoonbyul	33	\N
116	archivebyulyi	33	\N
117	byulgallery	33	\N
118	wheeinjpgs	34	\N
119	bestofwheein	34	\N
120	wheein_pics	34	\N
121	archivehwasa	35	\N
122	hwasagallery	35	\N
123	ahnhyejinpics	35	\N
124	ryujloops	1	\N
125	_somipics	36	\N
126	somsomiarchive	36	\N
127	somiloops	36	\N
128	karinaspics	37	\N
129	aespakarinapic	37	\N
130	karinaarchives	37	\N
131	karinapiics	37	\N
132	giselle_pics	38	\N
133	gisellepiics	38	\N
134	gisellespics	38	\N
135	GISELLEPIC	38	\N
136	winterpic	39	\N
137	minjeongallery	39	\N
138	wntrpics	39	\N
139	archivedwinter	39	\N
140	ningningpics	40	\N
141	ningningspics	40	\N
142	ningspics	40	\N
143	ningningfolder	40	\N
144	minseokpics	41	\N
145	minseokpcs	41	\N
146	archivejunmyeon	42	\N
147	suhopictures	42	\N
148	laypics_	43	\N
149	picszhang	43	\N
150	baekhyunpics	44	\N
151	baeksarchive	44	\N
152	cutekjdpics	45	\N
153	kjdpics	45	\N
154	chanyeol_pic	46	\N
155	pchanyeolpic	46	\N
156	DOpics2	47	\N
157	twelfthkelebek	47	\N
158	kimjipics	48	\N
159	jonginpic	48	\N
160	sehunspics	49	\N
161	hunarchive	49	\N
162	luhanpics	49	\N
163	archiveluhan	49	\N
164	wuyifan_pics	49	\N
166	hztpics	52	\N
168	huangzitaopics	52	\N
169	picsofdami	58	\N
170	hourly_dami	58	\N
171	Dami7Loops	58	\N
172	lghzone	59	\N
173	gahyeonpic	59	\N
174	lgarchive	59	\N
175	picsofhandong	56	\N
176	Hdloops	56	\N
177	hourlydong	56	\N
178	minjihourly	53	\N
179	kiminjipics	53	\N
180	MJKLOOKS	53	\N
181	siyeonhours	55	\N
182	siyeonhourly	55	\N
183	SuaHours	54	\N
184	suafiles	54	\N
185	queensualoops	54	\N
186	picsofyoohyeon	57	\N
187	hourlyoohyoen	57	\N
188	pics_yoohyeon	57	\N
\.


--
-- Data for Name: bot_twittermediasubscribedchannel; Type: TABLE DATA; Schema: public; Owner: kvdomingo
--

COPY public.bot_twittermediasubscribedchannel (id, channel_id, group_id) FROM stdin;
1	726831180565184603	1
3	727956565390524447	2
6	789385817884721164	3
7	796115017345925161	3
8	796115281733877820	3
9	796115281733877820	4
10	796115281733877820	11
11	796115281733877820	7
12	796115281733877820	5
13	796115281733877820	13
14	796115281733877820	12
15	796115281733877820	15
16	796115281733877820	16
17	796115281733877820	6
18	796115281733877820	17
20	803166633257598986	4
\.


--
-- Data for Name: bot_vlivesubscribedchannel; Type: TABLE DATA; Schema: public; Owner: kvdomingo
--

COPY public.bot_vlivesubscribedchannel (id, channel_id, group_id, dev_channel) FROM stdin;
1	726831180565184603	1	t
2	789385817884721164	3	t
3	727956565390524447	2	t
5	735600077296500826	3	f
6	735594245036965918	1	f
7	735600100604117073	2	f
8	735600148687618089	4	f
9	735600111345991740	5	f
10	735600135198867527	8	f
11	735600682291429387	7	f
12	778317997399212043	6	f
13	766754934271508501	3	f
14	785442350226735114	2	f
15	785442451951058964	6	f
16	785461972698923008	10	f
17	785461423186640937	3	f
18	785461675805507594	5	f
19	785461254663045160	1	f
20	785461857363165194	9	f
21	785461618620235816	7	f
22	785461786098401300	8	f
23	785461537770569728	4	f
24	785510309933613057	8	f
25	789686731829018644	1	f
26	789687273221259314	3	f
27	789687458409218108	6	f
28	789687904259538974	9	f
29	796115017345925161	6	f
30	796128406500147200	6	f
31	796128406500147200	2	f
32	796128406500147200	8	f
33	796128406500147200	15	f
34	796128406500147200	7	f
35	796128406500147200	17	f
36	796128406500147200	9	f
37	796128406500147200	4	f
38	796128406500147200	14	f
39	796128406500147200	16	f
40	796128406500147200	12	f
41	796128406500147200	3	f
42	787100433818714143	10	f
43	749506986697162792	6	f
44	749506986697162792	17	f
45	749506986697162792	13	f
46	749506986697162792	15	f
47	749506986697162792	10	f
48	749506986697162792	9	f
49	771064217070993438	10	f
50	816001543102922812	14	f
51	815999773517283369	14	f
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: kvdomingo
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2020-12-25 15:28:47.914+00	1	726831180565184603 (itzy)	2	[{"changed": {"fields": ["Dev channel"]}}]	3	1
2	2020-12-25 15:29:23.597+00	3	727956565390524447 (blackpink)	2	[{"changed": {"fields": ["Dev channel"]}}]	3	1
3	2020-12-26 11:24:11.107+00	1	itz (itzy)	1	[{"added": {}}]	7	1
4	2020-12-26 11:24:17.142+00	2	rv (redvelvet)	1	[{"added": {}}]	7	1
5	2020-12-26 11:24:30.366+00	3	mink (blackpink)	1	[{"added": {}}]	7	1
6	2020-12-26 11:24:44.572+00	4	more (twice)	1	[{"added": {}}]	7	1
7	2020-12-26 11:24:51.741+00	5	tdoong (twice)	1	[{"added": {}}]	7	1
8	2020-12-26 11:27:23.797+00	6	red-velvet (redvelvet)	1	[{"added": {}}]	7	1
9	2020-12-26 11:27:32.725+00	7	red_velvet (redvelvet)	1	[{"added": {}}]	7	1
10	2020-12-29 15:07:20.433+00	8	æ (aespa)	1	[{"added": {}}]	7	1
11	2021-01-02 11:53:30.169+00	1	itzy	2	[{"changed": {"fields": ["Vlive last seq"]}}]	1	1
12	2021-01-02 13:11:45.656+00	2	789385817884721164 (itzy)	3		4	1
13	2021-01-02 13:12:57.113+00	4	789385817884721164 (itzy)	3		4	1
14	2021-01-04 15:46:05.456+00	2	789385817884721164 (twice)	2	[{"changed": {"fields": ["Dev channel"]}}]	3	1
15	2021-01-04 15:49:56.185+00	3	twice	2	[{"changed": {"fields": ["Vlive last seq"]}}]	1	1
16	2021-01-04 15:56:01.886+00	3	twice	2	[{"changed": {"fields": ["Vlive last seq"]}}]	1	1
17	2021-01-04 15:57:58.028+00	3	twice	2	[{"changed": {"fields": ["Vlive last seq"]}}]	1	1
18	2021-01-04 15:59:03.163+00	1	itzy	2	[{"changed": {"fields": ["Vlive last seq"]}}]	1	1
19	2021-01-06 11:02:22.157+00	3	twice	2	[{"changed": {"fields": ["Twitter user name"]}}]	1	1
20	2021-01-06 15:26:14.683+00	2	BLACKPINK	2	[{"changed": {"fields": ["Name"]}}]	1	1
21	2021-01-06 15:26:22.424+00	6	BTS	2	[{"changed": {"fields": ["Name"]}}]	1	1
22	2021-01-06 15:26:36.225+00	1	ITZY	2	[{"changed": {"fields": ["Name"]}}]	1	1
23	2021-01-06 15:26:40.855+00	7	MAMAMOO	2	[{"changed": {"fields": ["Name"]}}]	1	1
24	2021-01-06 15:26:45.755+00	4	Red Velvet	2	[{"changed": {"fields": ["Name"]}}]	1	1
25	2021-01-06 15:26:51.176+00	8	Somi	2	[{"changed": {"fields": ["Name"]}}]	1	1
26	2021-01-06 15:26:54.965+00	3	TWICE	2	[{"changed": {"fields": ["Name"]}}]	1	1
27	2021-01-06 15:27:01.504+00	5	IU	2	[{"changed": {"fields": ["Name"]}}]	1	1
28	2021-01-06 15:27:51.165+00	10	EXO	2	[{"changed": {"fields": ["Name"]}}]	1	1
29	2021-01-06 15:30:40.74+00	9	aespa	2	[{"changed": {"fields": ["Vlive channel code"]}}]	1	1
30	2021-01-06 15:31:49.189+00	11	Dreamcatcher	1	[{"added": {}}]	1	1
31	2021-01-06 15:32:12.477+00	9	insomnia (Dreamcatcher)	1	[{"added": {}}]	7	1
32	2021-01-06 15:32:26.339+00	10	redvelvet (Red Velvet)	1	[{"added": {}}]	7	1
33	2021-01-06 15:32:45.99+00	11	teudoong (TWICE)	1	[{"added": {}}]	7	1
34	2021-01-06 15:34:52.117+00	53	JiU (Dreamcatcher)	1	[{"added": {}}]	2	1
35	2021-01-06 15:35:40.679+00	53	JiU (Dreamcatcher)	2	[{"changed": {"fields": ["English name"]}}]	2	1
36	2021-01-06 15:36:02.596+00	54	SuA (Dreamcatcher)	1	[{"added": {}}]	2	1
37	2021-01-06 15:36:30.146+00	55	Siyeon (Dreamcatcher)	1	[{"added": {}}]	2	1
38	2021-01-06 15:36:54.183+00	56	Handong (Dreamcatcher)	1	[{"added": {}}]	2	1
39	2021-01-06 15:37:40.858+00	57	Yoohyeon (Dreamcatcher)	1	[{"added": {}}]	2	1
40	2021-01-06 15:40:14.259+00	53	JiU (Dreamcatcher)	2	[{"changed": {"fields": ["Birthday"]}}]	2	1
41	2021-01-06 15:40:38.436+00	54	SuA (Dreamcatcher)	2	[{"changed": {"fields": ["Birthday"]}}]	2	1
42	2021-01-06 15:41:45.266+00	55	Siyeon (Dreamcatcher)	2	[{"changed": {"fields": ["Birthday"]}}]	2	1
43	2021-01-06 15:42:02.304+00	56	Handong (Dreamcatcher)	2	[{"changed": {"fields": ["Birthday"]}}]	2	1
44	2021-01-06 15:42:48.881+00	58	Dami (Dreamcatcher)	1	[{"added": {}}]	2	1
45	2021-01-06 15:43:54.101+00	59	Gahyeon (Dreamcatcher)	1	[{"added": {}}]	2	1
46	2021-01-06 16:01:38.95+00	17	Chaeyoung (TWICE)	2	[{"added": {"name": "member alias", "object": "seyoung (Chaeyoung of TWICE)"}}, {"added": {"name": "member alias", "object": "chiyong (Chaeyoung of TWICE)"}}, {"added": {"name": "member alias", "object": "siyong (Chaeyoung of TWICE)"}}]	2	1
47	2021-01-06 16:02:07.748+00	17	Chaeyoung (TWICE)	2	[{"added": {"name": "member alias", "object": "seyoung (Chaeyoung of TWICE)"}}, {"added": {"name": "member alias", "object": "chiyong (Chaeyoung of TWICE)"}}, {"added": {"name": "member alias", "object": "siyong (Chaeyoung of TWICE)"}}]	2	1
48	2021-01-06 16:04:31.35+00	3	TWICE	2	[{"changed": {"name": "member", "object": "Chaeyoung (TWICE)", "fields": ["Birthday"]}}, {"changed": {"name": "member", "object": "Dahyun (TWICE)", "fields": ["Birthday"]}}, {"changed": {"name": "member", "object": "Jeongyeon (TWICE)", "fields": ["Birthday"]}}, {"changed": {"name": "member", "object": "Jihyo (TWICE)", "fields": ["Birthday"]}}, {"changed": {"name": "member", "object": "Mina (TWICE)", "fields": ["Birthday"]}}, {"changed": {"name": "member", "object": "Momo (TWICE)", "fields": ["Birthday"]}}, {"changed": {"name": "member", "object": "Nayeon (TWICE)", "fields": ["Birthday"]}}, {"changed": {"name": "member", "object": "Sana (TWICE)", "fields": ["Birthday"]}}, {"changed": {"name": "member", "object": "Tzuyu (TWICE)", "fields": ["Birthday"]}}]	1	1
49	2021-01-06 16:13:05.659+00	58	Dami (Dreamcatcher)	2	[{"added": {"name": "twitter media source", "object": "picsofdami (for Dami of Dreamcatcher)"}}, {"added": {"name": "twitter media source", "object": "hourly_dami (for Dami of Dreamcatcher)"}}, {"added": {"name": "twitter media source", "object": "Dami7Loops (for Dami of Dreamcatcher)"}}]	2	1
50	2021-01-06 16:14:19.182+00	59	Gahyeon (Dreamcatcher)	2	[{"added": {"name": "member alias", "object": "maknae (Gahyeon of Dreamcatcher)"}}, {"added": {"name": "twitter media source", "object": "lghzone (for Gahyeon of Dreamcatcher)"}}, {"added": {"name": "twitter media source", "object": "gahyeonpic (for Gahyeon of Dreamcatcher)"}}, {"added": {"name": "twitter media source", "object": "lgarchive (for Gahyeon of Dreamcatcher)"}}]	2	1
51	2021-01-06 16:17:24.139+00	56	Handong (Dreamcatcher)	2	[{"added": {"name": "twitter media source", "object": "picsofhandong (for Handong of Dreamcatcher)"}}, {"added": {"name": "twitter media source", "object": "Hdloops (for Handong of Dreamcatcher)"}}, {"added": {"name": "twitter media source", "object": "hourlydong (for Handong of Dreamcatcher)"}}]	2	1
52	2021-01-06 16:18:51.802+00	53	JiU (Dreamcatcher)	2	[{"added": {"name": "twitter media source", "object": "minjihourly (for JiU of Dreamcatcher)"}}, {"added": {"name": "twitter media source", "object": "kiminjipics (for JiU of Dreamcatcher)"}}, {"added": {"name": "twitter media source", "object": "MJKLOOKS (for JiU of Dreamcatcher)"}}]	2	1
53	2021-01-06 16:21:39.846+00	55	Siyeon (Dreamcatcher)	2	[{"added": {"name": "twitter media source", "object": "siyeonhours (for Siyeon of Dreamcatcher)"}}, {"added": {"name": "twitter media source", "object": "siyeonhourly (for Siyeon of Dreamcatcher)"}}]	2	1
54	2021-01-06 16:25:11.765+00	54	SuA (Dreamcatcher)	2	[{"added": {"name": "twitter media source", "object": "SuaHours (for SuA of Dreamcatcher)"}}, {"added": {"name": "twitter media source", "object": "suafiles (for SuA of Dreamcatcher)"}}, {"added": {"name": "twitter media source", "object": "queensualoops (for SuA of Dreamcatcher)"}}]	2	1
55	2021-01-06 16:27:04.378+00	57	Yoohyeon (Dreamcatcher)	2	[{"added": {"name": "twitter media source", "object": "picsofyoohyeon (for Yoohyeon of Dreamcatcher)"}}, {"added": {"name": "twitter media source", "object": "hourlyoohyoen (for Yoohyeon of Dreamcatcher)"}}, {"added": {"name": "twitter media source", "object": "pics_yoohyeon (for Yoohyeon of Dreamcatcher)"}}]	2	1
56	2021-01-07 11:35:27.985+00	24	IU (IU)	2	[{"changed": {"fields": ["Birthday"]}}]	2	1
57	2021-01-07 11:38:12.415+00	4	Red Velvet	2	[{"changed": {"name": "member", "object": "Irene (Red Velvet)", "fields": ["Birthday"]}}, {"changed": {"name": "member", "object": "Joy (Red Velvet)", "fields": ["Birthday"]}}, {"changed": {"name": "member", "object": "Seulgi (Red Velvet)", "fields": ["Birthday"]}}, {"changed": {"name": "member", "object": "Wendy (Red Velvet)", "fields": ["Birthday"]}}, {"changed": {"name": "member", "object": "Yeri (Red Velvet)", "fields": ["Birthday"]}}]	1	1
58	2021-01-07 11:39:30.929+00	36	Somi (Somi)	2	[{"changed": {"fields": ["English name", "Birthday"]}}]	2	1
59	2021-01-07 11:42:00.119+00	1	ITZY	2	[{"changed": {"name": "member", "object": "Chaeryeong (ITZY)", "fields": ["English name", "Birthday"]}}, {"changed": {"name": "member", "object": "Lia (ITZY)", "fields": ["English name", "Birthday"]}}, {"changed": {"name": "member", "object": "Ryujin (ITZY)", "fields": ["English name", "Birthday"]}}, {"changed": {"name": "member", "object": "Yeji (ITZY)", "fields": ["English name", "Birthday"]}}, {"changed": {"name": "member", "object": "Yuna (ITZY)", "fields": ["English name", "Birthday"]}}]	1	1
60	2021-01-07 11:44:57.236+00	7	MAMAMOO	2	[{"changed": {"name": "member", "object": "Hwasa (MAMAMOO)", "fields": ["Birthday"]}}, {"changed": {"name": "member", "object": "Moonbyul (MAMAMOO)", "fields": ["Birthday"]}}, {"changed": {"name": "member", "object": "Solar (MAMAMOO)", "fields": ["Birthday"]}}, {"changed": {"name": "member", "object": "Wheein (MAMAMOO)", "fields": ["Birthday"]}}]	1	1
61	2021-01-07 11:46:55.432+00	2	BLACKPINK	2	[{"changed": {"name": "member", "object": "Jennie (BLACKPINK)", "fields": ["Birthday"]}}, {"changed": {"name": "member", "object": "Jisoo (BLACKPINK)", "fields": ["Birthday"]}}, {"changed": {"name": "member", "object": "Lisa (BLACKPINK)", "fields": ["Given name", "English name", "Birthday"]}}, {"changed": {"name": "member", "object": "Ros\\u00e9 (BLACKPINK)", "fields": ["Birthday"]}}]	1	1
62	2021-01-07 11:48:34.838+00	9	aespa	2	[{"changed": {"name": "member", "object": "Giselle (aespa)", "fields": ["Birthday"]}}, {"changed": {"name": "member", "object": "Karina (aespa)", "fields": ["Birthday"]}}, {"changed": {"name": "member", "object": "Ningning (aespa)", "fields": ["Birthday"]}}, {"changed": {"name": "member", "object": "Winter (aespa)", "fields": ["Birthday"]}}]	1	1
63	2021-01-07 11:52:29.075+00	6	BTS	2	[{"added": {"name": "group alias", "object": "bangtan (BTS)"}}, {"added": {"name": "group alias", "object": "sonyeondan (BTS)"}}, {"added": {"name": "group alias", "object": "bangtan boys (BTS)"}}, {"changed": {"name": "member", "object": "J-Hope (BTS)", "fields": ["Birthday"]}}, {"changed": {"name": "member", "object": "Jimin (BTS)", "fields": ["Birthday"]}}, {"changed": {"name": "member", "object": "Jin (BTS)", "fields": ["Birthday"]}}, {"changed": {"name": "member", "object": "Jungkook (BTS)", "fields": ["Birthday"]}}, {"changed": {"name": "member", "object": "RM (BTS)", "fields": ["Birthday"]}}, {"changed": {"name": "member", "object": "Suga (BTS)", "fields": ["Birthday"]}}, {"changed": {"name": "member", "object": "V (BTS)", "fields": ["Birthday"]}}]	1	1
64	2021-01-07 12:00:00.492+00	10	EXO	2	[{"changed": {"name": "member", "object": "Baekhyun (EXO)", "fields": ["English name", "Birthday"]}}, {"changed": {"name": "member", "object": "Chanyeol (EXO)", "fields": ["English name", "Birthday"]}}, {"changed": {"name": "member", "object": "Chen (EXO)", "fields": ["English name", "Birthday"]}}, {"changed": {"name": "member", "object": "D.O. (EXO)", "fields": ["English name", "Birthday"]}}, {"changed": {"name": "member", "object": "Kai (EXO)", "fields": ["English name", "Birthday"]}}, {"changed": {"name": "member", "object": "Kris (EXO)", "fields": ["English name", "Birthday"]}}, {"changed": {"name": "member", "object": "Lay (EXO)", "fields": ["Given name", "English name", "Birthday"]}}, {"changed": {"name": "member", "object": "Luhan (EXO)", "fields": ["Birthday"]}}, {"changed": {"name": "member", "object": "Sehun (EXO)", "fields": ["English name", "Birthday"]}}, {"changed": {"name": "member", "object": "Suho (EXO)", "fields": ["English name", "Birthday"]}}, {"changed": {"name": "member", "object": "Tao (EXO)", "fields": ["Birthday"]}}, {"changed": {"name": "member", "object": "Xiumin (EXO)", "fields": ["English name", "Birthday"]}}]	1	1
65	2021-01-07 12:04:38.454+00	12	CLC	1	[{"added": {}}, {"added": {"name": "member", "object": "Seungyeon (CLC)"}}, {"added": {"name": "member", "object": "Seunghee (CLC)"}}, {"added": {"name": "member", "object": "Yujin (CLC)"}}, {"added": {"name": "member", "object": "Sorn (CLC)"}}, {"added": {"name": "member", "object": "Yeeun (CLC)"}}, {"added": {"name": "member", "object": "Eunbin (CLC)"}}, {"added": {"name": "member", "object": "Elkie (CLC)"}}]	1	1
66	2021-01-07 12:06:19.519+00	13	Chungha	1	[{"added": {}}, {"added": {"name": "member", "object": "Chungha (Chungha)"}}]	1	1
67	2021-01-07 12:08:15.845+00	13	Chungha	2	[]	1	1
68	2021-01-07 12:13:56.751+00	14	IZ*ONE	1	[{"added": {}}, {"added": {"name": "group alias", "object": "izone (IZ*ONE)"}}, {"added": {"name": "member", "object": "Eunbi (IZ*ONE)"}}, {"added": {"name": "member", "object": "Sakura (IZ*ONE)"}}, {"added": {"name": "member", "object": "Hyewon (IZ*ONE)"}}, {"added": {"name": "member", "object": "Yena (IZ*ONE)"}}, {"added": {"name": "member", "object": "Chaeyeon (IZ*ONE)"}}, {"added": {"name": "member", "object": "Chaewon (IZ*ONE)"}}, {"added": {"name": "member", "object": "Minju (IZ*ONE)"}}, {"added": {"name": "member", "object": "Nako (IZ*ONE)"}}, {"added": {"name": "member", "object": "Hitomi (IZ*ONE)"}}, {"added": {"name": "member", "object": "Yuri (IZ*ONE)"}}, {"added": {"name": "member", "object": "Yujin (IZ*ONE)"}}, {"added": {"name": "member", "object": "Wonyoung (IZ*ONE)"}}]	1	1
69	2021-01-07 12:17:08.305+00	15	(G)I-DLE	1	[{"added": {}}, {"added": {"name": "group alias", "object": "gidle ((G)I-DLE)"}}, {"added": {"name": "member", "object": "Soyeon ((G)I-DLE)"}}, {"added": {"name": "member", "object": "Miyeon ((G)I-DLE)"}}, {"added": {"name": "member", "object": "Minnie ((G)I-DLE)"}}, {"added": {"name": "member", "object": "Soojin ((G)I-DLE)"}}, {"added": {"name": "member", "object": "Yuqi ((G)I-DLE)"}}, {"added": {"name": "member", "object": "Shuhua ((G)I-DLE)"}}]	1	1
70	2021-01-07 12:25:41.464+00	16	LOOΠΔ	1	[{"added": {}}, {"added": {"name": "group alias", "object": "loona (LOO\\u03a0\\u0394)"}}, {"added": {"name": "group alias", "object": "idalwi sonyeo (LOO\\u03a0\\u0394)"}}, {"added": {"name": "member", "object": "Haseul (LOO\\u03a0\\u0394)"}}, {"added": {"name": "member", "object": "Vivi (LOO\\u03a0\\u0394)"}}, {"added": {"name": "member", "object": "Yves (LOO\\u03a0\\u0394)"}}, {"added": {"name": "member", "object": "Jinsoul (LOO\\u03a0\\u0394)"}}, {"added": {"name": "member", "object": "Kim Lip (LOO\\u03a0\\u0394)"}}, {"added": {"name": "member", "object": "Chuu (LOO\\u03a0\\u0394)"}}, {"added": {"name": "member", "object": "Heejin (LOO\\u03a0\\u0394)"}}, {"added": {"name": "member", "object": "Hyunjin (LOO\\u03a0\\u0394)"}}, {"added": {"name": "member", "object": "Go Won (LOO\\u03a0\\u0394)"}}, {"added": {"name": "member", "object": "Choerry (LOO\\u03a0\\u0394)"}}, {"added": {"name": "member", "object": "Olivia Hye (LOO\\u03a0\\u0394)"}}, {"added": {"name": "member", "object": "Yeojin (LOO\\u03a0\\u0394)"}}]	1	1
71	2021-01-07 12:26:27.959+00	9	æspa	2	[{"changed": {"fields": ["Name"]}}, {"added": {"name": "group alias", "object": "aespa (\\u00e6spa)"}}]	1	1
72	2021-01-07 12:29:37.215+00	17	SHINee	1	[{"added": {}}, {"added": {"name": "member", "object": "Onew (SHINee)"}}, {"added": {"name": "member", "object": "Key (SHINee)"}}, {"added": {"name": "member", "object": "Minho (SHINee)"}}, {"added": {"name": "member", "object": "Taemin (SHINee)"}}, {"added": {"name": "member", "object": "Jonghyun (SHINee)"}}]	1	1
73	2021-01-07 12:32:20.847+00	3	TWICE	2	[{"added": {"name": "group alias", "object": "\\ud2b8\\uc640\\uc774\\uc2a4 (TWICE)"}}]	1	1
74	2021-01-07 12:36:41.76+00	15	(G)I-DLE	2	[{"changed": {"fields": ["Korean name"]}}]	1	1
75	2021-01-07 12:38:10.308+00	9	æspa (에스파)	2	[{"changed": {"fields": ["Korean name"]}}]	1	1
76	2021-01-07 12:39:48.274+00	2	BLACKPINK (블랙핑크)	2	[{"changed": {"fields": ["Korean name"]}}]	1	1
77	2021-01-07 12:40:51.904+00	6	BTS (방탄 손연단)	2	[{"changed": {"fields": ["Korean name"]}}]	1	1
78	2021-01-07 12:41:47.643+00	13	Chungha (청하)	2	[{"changed": {"fields": ["Korean name"]}}]	1	1
79	2021-01-07 12:44:19.785+00	12	CLC (씨엘씨)	2	[{"changed": {"fields": ["Korean name"]}}]	1	1
80	2021-01-07 12:45:23.009+00	11	Dreamcatcher (드림 캐쳐)	2	[{"changed": {"fields": ["Korean name"]}}]	1	1
81	2021-01-07 12:46:31.913+00	10	EXO (엑소)	2	[{"changed": {"fields": ["Korean name"]}}]	1	1
82	2021-01-07 12:47:05.253+00	1	ITZY (있지)	2	[{"changed": {"fields": ["Korean name"]}}]	1	1
83	2021-01-07 12:47:31.939+00	5	IU (아이유)	2	[{"changed": {"fields": ["Korean name"]}}]	1	1
84	2021-01-07 12:48:12.701+00	14	IZ*ONE (아이즈원)	2	[{"changed": {"fields": ["Korean name"]}}]	1	1
85	2021-01-07 12:48:42.962+00	16	LOOΠΔ (이달의 소녀)	2	[{"changed": {"fields": ["Korean name"]}}]	1	1
86	2021-01-07 12:49:04.144+00	7	MAMAMOO (마마무)	2	[{"changed": {"fields": ["Korean name"]}}]	1	1
87	2021-01-07 12:50:01.48+00	4	Red Velvet (레드 벨벳)	2	[{"changed": {"fields": ["Korean name"]}}]	1	1
88	2021-01-07 12:50:29.852+00	17	SHINee (샤이니)	2	[{"changed": {"fields": ["Korean name"]}}]	1	1
89	2021-01-07 12:50:44.306+00	8	Somi (소미)	2	[{"changed": {"fields": ["Korean name"]}}]	1	1
90	2021-01-07 12:51:01.129+00	3	TWICE (트와이스)	2	[{"changed": {"fields": ["Korean name"]}}]	1	1
91	2021-01-08 13:56:34.343+00	3	TWICE (트와이스)	2	[{"changed": {"name": "member", "object": "Nayeon (TWICE)", "fields": ["Korean name"]}}]	1	1
92	2021-01-08 14:03:10.45+00	3	TWICE (트와이스)	2	[{"changed": {"name": "member", "object": "Jeongyeon (TWICE)", "fields": ["Korean name"]}}, {"changed": {"name": "member", "object": "Momo (TWICE)", "fields": ["Korean name"]}}, {"changed": {"name": "member", "object": "Sana (TWICE)", "fields": ["Korean name"]}}, {"changed": {"name": "member", "object": "Jihyo (TWICE)", "fields": ["Korean name"]}}, {"changed": {"name": "member", "object": "Mina (TWICE)", "fields": ["Korean name"]}}, {"changed": {"name": "member", "object": "Dahyun (TWICE)", "fields": ["Korean name"]}}, {"changed": {"name": "member", "object": "Chaeyoung (TWICE)", "fields": ["Korean name"]}}, {"changed": {"name": "member", "object": "Tzuyu (TWICE)", "fields": ["Korean name"]}}]	1	1
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: kvdomingo
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	bot	group
2	bot	member
3	bot	vlivesubscribedchannel
4	bot	twittermediasubscribedchannel
5	bot	twittermediasource
6	bot	memberalias
7	bot	groupalias
8	admin	logentry
9	auth	permission
10	auth	group
11	auth	user
12	contenttypes	contenttype
13	sessions	session
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: kvdomingo
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2021-01-08 15:18:27.647666+00
2	auth	0001_initial	2021-01-08 15:18:27.803727+00
3	admin	0001_initial	2021-01-08 15:18:28.043224+00
4	admin	0002_logentry_remove_auto_add	2021-01-08 15:18:28.171791+00
5	admin	0003_logentry_add_action_flag_choices	2021-01-08 15:18:28.297593+00
6	contenttypes	0002_remove_content_type_name	2021-01-08 15:18:28.52423+00
7	auth	0002_alter_permission_name_max_length	2021-01-08 15:18:28.627635+00
8	auth	0003_alter_user_email_max_length	2021-01-08 15:18:28.751569+00
9	auth	0004_alter_user_username_opts	2021-01-08 15:18:28.803624+00
10	auth	0005_alter_user_last_login_null	2021-01-08 15:18:28.868148+00
11	auth	0006_require_contenttypes_0002	2021-01-08 15:18:28.89528+00
12	auth	0007_alter_validators_add_error_messages	2021-01-08 15:18:28.963358+00
13	auth	0008_alter_user_username_max_length	2021-01-08 15:18:29.043163+00
14	auth	0009_alter_user_last_name_max_length	2021-01-08 15:18:29.128966+00
15	auth	0010_alter_group_name_max_length	2021-01-08 15:18:29.221158+00
16	auth	0011_update_proxy_permissions	2021-01-08 15:18:29.287149+00
17	auth	0012_alter_user_first_name_max_length	2021-01-08 15:18:29.388542+00
18	bot	0001_initial	2021-01-08 15:18:29.784837+00
19	bot	0002_auto_20201225_2253	2021-01-08 15:18:30.031794+00
20	bot	0003_twittermediasource_last_tweet_id	2021-01-08 15:18:30.166282+00
21	bot	0004_vlivesubscribedchannel_dev_channel	2021-01-08 15:18:30.293922+00
22	bot	0005_auto_20201225_2343	2021-01-08 15:18:30.631679+00
23	bot	0006_activate_pg_ext_20201226_2344	2021-01-08 15:18:30.781483+00
24	bot	0007_auto_20210102_2104	2021-01-08 15:18:31.0414+00
25	bot	0008_auto_20210106_2327	2021-01-08 15:18:31.135065+00
26	bot	0009_auto_20210106_2334	2021-01-08 15:18:31.20413+00
27	bot	0010_auto_20210107_0001	2021-01-08 15:18:31.320181+00
28	bot	0011_auto_20210107_2035	2021-01-08 15:18:31.378242+00
29	bot	0012_auto_20210108_2154	2021-01-08 15:18:31.554277+00
30	bot	0013_member_native_name	2021-01-08 15:18:31.631261+00
31	bot	0014_auto_20210108_2238	2021-01-08 15:18:31.885414+00
32	sessions	0001_initial	2021-01-08 15:18:31.978113+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: kvdomingo
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
7yvllpzvq997ooxujoh5bmpigve4f1xc	.eJxVjEEOwiAQRe_C2pAZGhjq0r1nIMBMpWogKe3KeHdt0oVu_3vvv1SI21rC1mUJM6uzQnX63VLMD6k74Hust6Zzq-syJ70r-qBdXxvL83K4fwcl9vKtSQCzCMPIaLIDNwllZ2wC4w2x82jtMMKEAxvywEYQkBzZOAgl8Or9AdBsNtk:1kvfTC:-OesF1SUIWoqk7rsZqZeJsIls7qoEi0JbomjsUGc2FA	2021-01-16 11:53:18.37+00
jb3e3v7ierqkrm5v4srfa7eq506hd5pl	.eJxVjEEOwiAQRe_C2pAZGhjq0r1nIMBMpWogKe3KeHdt0oVu_3vvv1SI21rC1mUJM6uzQnX63VLMD6k74Hust6Zzq-syJ70r-qBdXxvL83K4fwcl9vKtSQCzCMPIaLIDNwllZ2wC4w2x82jtMMKEAxvywEYQkBzZOAgl8Or9AdBsNtk:1ksoDm:dxHda0VZZBqKFRE2GykggmC0yJhsgDvXAkI1tnVUs9k	2021-01-08 14:37:34.198+00
r2oz6u8c4vjy66cfu2vsw5qvlzz2l2s8	.eJxVjEEOwiAQRe_C2pAZGhjq0r1nIMBMpWogKe3KeHdt0oVu_3vvv1SI21rC1mUJM6uzQnX63VLMD6k74Hust6Zzq-syJ70r-qBdXxvL83K4fwcl9vKtSQCzCMPIaLIDNwllZ2wC4w2x82jtMMKEAxvywEYQkBzZOAgl8Or9AdBsNtk:1kxsvW:g_5sbTN20BHX4rxbcgOhdszma9D5ZayfU-gk0IlNdW0	2021-01-22 14:39:42.826+00
li5mn4ug75zwdf8w7dsytz6qo2d4e9q7	.eJxVjEEOwiAQRe_C2pAZGhjq0r1nIMBMpWogKe3KeHdt0oVu_3vvv1SI21rC1mUJM6uzQnX63VLMD6k74Hust6Zzq-syJ70r-qBdXxvL83K4fwcl9vKtSQCzCMPIaLIDNwllZ2wC4w2x82jtMMKEAxvywEYQkBzZOAgl8Or9AdBsNtk:1kxtsx:CWwKrxoSxJMKUqis70I_hk8IvXDoQ2_EDBUfYe6H2mE	2021-01-22 15:41:07.926644+00
o93ejgw2iff5pu3sm234yxeaol6hrr4d	.eJxVjEEOwiAQRe_C2pAZGhjq0r1nIMBMpWogKe3KeHdt0oVu_3vvv1SI21rC1mUJM6uzQnX63VLMD6k74Hust6Zzq-syJ70r-qBdXxvL83K4fwcl9vKtSQCzCMPIaLIDNwllZ2wC4w2x82jtMMKEAxvywEYQkBzZOAgl8Or9AdBsNtk:1kyCbs:zwmnAsvGx5VLa5fdkJ2mkYa2UBJ4VWtysKJ8ayMwXJ0	2021-01-23 11:40:44.266244+00
zyztemu0ogg52rfzlguj45ajzy03al41	.eJxVjEEOwiAQRe_C2pAZGhjq0r1nIMBMpWogKe3KeHdt0oVu_3vvv1SI21rC1mUJM6uzQnX63VLMD6k74Hust6Zzq-syJ70r-qBdXxvL83K4fwcl9vKtSQCzCMPIaLIDNwllZ2wC4w2x82jtMMKEAxvywEYQkBzZOAgl8Or9AdBsNtk:1l4383:Q6843x777qPKfivafqemoM67vU6Xu2ABA6s_biv3ECM	2021-02-08 14:46:07.504476+00
\.


--
-- Data for Name: group; Type: TABLE DATA; Schema: public; Owner: kvdomingo
--

COPY public."group" (id, name, vlive_channel_code, vlive_channel_seq, vlive_last_seq) FROM stdin;
\.


--
-- Data for Name: member; Type: TABLE DATA; Schema: public; Owner: kvdomingo
--

COPY public.member (id, stage_name, given_name, family_name, group_id, birthday) FROM stdin;
\.


--
-- Data for Name: twitteraccount; Type: TABLE DATA; Schema: public; Owner: kvdomingo
--

COPY public.twitteraccount (id, account_name, member_id, last_tweet_id) FROM stdin;
\.


--
-- Data for Name: twitterchannel; Type: TABLE DATA; Schema: public; Owner: kvdomingo
--

COPY public.twitterchannel (id, channel_id, group_id) FROM stdin;
\.


--
-- Data for Name: vlivechannel; Type: TABLE DATA; Schema: public; Owner: kvdomingo
--

COPY public.vlivechannel (id, channel_id, group_id) FROM stdin;
\.


--
-- Name: alias_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kvdomingo
--

SELECT pg_catalog.setval('public.alias_id_seq', 1, false);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kvdomingo
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kvdomingo
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kvdomingo
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 52, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kvdomingo
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kvdomingo
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 1, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kvdomingo
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: bot_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kvdomingo
--

SELECT pg_catalog.setval('public.bot_group_id_seq', 17, true);


--
-- Name: bot_groupalias_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kvdomingo
--

SELECT pg_catalog.setval('public.bot_groupalias_id_seq', 20, true);


--
-- Name: bot_member_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kvdomingo
--

SELECT pg_catalog.setval('public.bot_member_id_seq', 102, true);


--
-- Name: bot_memberalias_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kvdomingo
--

SELECT pg_catalog.setval('public.bot_memberalias_id_seq', 59, true);


--
-- Name: bot_twittermediasource_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kvdomingo
--

SELECT pg_catalog.setval('public.bot_twittermediasource_id_seq', 188, true);


--
-- Name: bot_twittermediasubscribedchannel_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kvdomingo
--

SELECT pg_catalog.setval('public.bot_twittermediasubscribedchannel_id_seq', 20, true);


--
-- Name: bot_vlivesubscribedchannel_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kvdomingo
--

SELECT pg_catalog.setval('public.bot_vlivesubscribedchannel_id_seq', 51, true);


--
-- Name: channel_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kvdomingo
--

SELECT pg_catalog.setval('public.channel_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kvdomingo
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 92, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kvdomingo
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 13, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kvdomingo
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 32, true);


--
-- Name: group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kvdomingo
--

SELECT pg_catalog.setval('public.group_id_seq', 1, false);


--
-- Name: member_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kvdomingo
--

SELECT pg_catalog.setval('public.member_id_seq', 1, false);


--
-- Name: twitteraccount_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kvdomingo
--

SELECT pg_catalog.setval('public.twitteraccount_id_seq', 1, false);


--
-- Name: vlivechannel_id_seq; Type: SEQUENCE SET; Schema: public; Owner: kvdomingo
--

SELECT pg_catalog.setval('public.vlivechannel_id_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: alias alias_pkey; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.alias
    ADD CONSTRAINT alias_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: bot_group bot_group_name_key; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.bot_group
    ADD CONSTRAINT bot_group_name_key UNIQUE (name);


--
-- Name: bot_group bot_group_pkey; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.bot_group
    ADD CONSTRAINT bot_group_pkey PRIMARY KEY (id);


--
-- Name: bot_groupalias bot_groupalias_alias_key; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.bot_groupalias
    ADD CONSTRAINT bot_groupalias_alias_key UNIQUE (alias);


--
-- Name: bot_groupalias bot_groupalias_pkey; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.bot_groupalias
    ADD CONSTRAINT bot_groupalias_pkey PRIMARY KEY (id);


--
-- Name: bot_member bot_member_pkey; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.bot_member
    ADD CONSTRAINT bot_member_pkey PRIMARY KEY (id);


--
-- Name: bot_memberalias bot_memberalias_pkey; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.bot_memberalias
    ADD CONSTRAINT bot_memberalias_pkey PRIMARY KEY (id);


--
-- Name: bot_twittermediasource bot_twittermediasource_account_name_key; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.bot_twittermediasource
    ADD CONSTRAINT bot_twittermediasource_account_name_key UNIQUE (account_name);


--
-- Name: bot_twittermediasource bot_twittermediasource_pkey; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.bot_twittermediasource
    ADD CONSTRAINT bot_twittermediasource_pkey PRIMARY KEY (id);


--
-- Name: bot_twittermediasubscribedchannel bot_twittermediasubscrib_channel_id_group_id_0536155e_uniq; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.bot_twittermediasubscribedchannel
    ADD CONSTRAINT bot_twittermediasubscrib_channel_id_group_id_0536155e_uniq UNIQUE (channel_id, group_id);


--
-- Name: bot_twittermediasubscribedchannel bot_twittermediasubscribedchannel_pkey; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.bot_twittermediasubscribedchannel
    ADD CONSTRAINT bot_twittermediasubscribedchannel_pkey PRIMARY KEY (id);


--
-- Name: bot_vlivesubscribedchannel bot_vlivesubscribedchannel_channel_id_group_id_d5bde456_uniq; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.bot_vlivesubscribedchannel
    ADD CONSTRAINT bot_vlivesubscribedchannel_channel_id_group_id_d5bde456_uniq UNIQUE (channel_id, group_id);


--
-- Name: bot_vlivesubscribedchannel bot_vlivesubscribedchannel_pkey; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.bot_vlivesubscribedchannel
    ADD CONSTRAINT bot_vlivesubscribedchannel_pkey PRIMARY KEY (id);


--
-- Name: twitterchannel channel_pkey; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.twitterchannel
    ADD CONSTRAINT channel_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: group group_name_key; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public."group"
    ADD CONSTRAINT group_name_key UNIQUE (name);


--
-- Name: group group_pkey; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public."group"
    ADD CONSTRAINT group_pkey PRIMARY KEY (id);


--
-- Name: member member_pkey; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.member
    ADD CONSTRAINT member_pkey PRIMARY KEY (id);


--
-- Name: twitteraccount twitteraccount_pkey; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.twitteraccount
    ADD CONSTRAINT twitteraccount_pkey PRIMARY KEY (id);


--
-- Name: vlivechannel vlivechannel_pkey; Type: CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.vlivechannel
    ADD CONSTRAINT vlivechannel_pkey PRIMARY KEY (id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: kvdomingo
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: kvdomingo
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: kvdomingo
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: kvdomingo
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: kvdomingo
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: kvdomingo
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: kvdomingo
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: kvdomingo
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: kvdomingo
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: bot_group_name_b43d5675_like; Type: INDEX; Schema: public; Owner: kvdomingo
--

CREATE INDEX bot_group_name_b43d5675_like ON public.bot_group USING btree (name varchar_pattern_ops);


--
-- Name: bot_groupalias_alias_54116823_like; Type: INDEX; Schema: public; Owner: kvdomingo
--

CREATE INDEX bot_groupalias_alias_54116823_like ON public.bot_groupalias USING btree (alias varchar_pattern_ops);


--
-- Name: bot_groupalias_group_id_e557ec2e; Type: INDEX; Schema: public; Owner: kvdomingo
--

CREATE INDEX bot_groupalias_group_id_e557ec2e ON public.bot_groupalias USING btree (group_id);


--
-- Name: bot_member_group_id_1298951f; Type: INDEX; Schema: public; Owner: kvdomingo
--

CREATE INDEX bot_member_group_id_1298951f ON public.bot_member USING btree (group_id);


--
-- Name: bot_memberalias_member_id_b75dc052; Type: INDEX; Schema: public; Owner: kvdomingo
--

CREATE INDEX bot_memberalias_member_id_b75dc052 ON public.bot_memberalias USING btree (member_id);


--
-- Name: bot_twittermediasource_account_name_11a198f1_like; Type: INDEX; Schema: public; Owner: kvdomingo
--

CREATE INDEX bot_twittermediasource_account_name_11a198f1_like ON public.bot_twittermediasource USING btree (account_name varchar_pattern_ops);


--
-- Name: bot_twittermediasource_member_id_b1811a24; Type: INDEX; Schema: public; Owner: kvdomingo
--

CREATE INDEX bot_twittermediasource_member_id_b1811a24 ON public.bot_twittermediasource USING btree (member_id);


--
-- Name: bot_twittermediasubscribedchannel_group_id_e9c4b8a7; Type: INDEX; Schema: public; Owner: kvdomingo
--

CREATE INDEX bot_twittermediasubscribedchannel_group_id_e9c4b8a7 ON public.bot_twittermediasubscribedchannel USING btree (group_id);


--
-- Name: bot_vlivesubscribedchannel_group_id_5ac41767; Type: INDEX; Schema: public; Owner: kvdomingo
--

CREATE INDEX bot_vlivesubscribedchannel_group_id_5ac41767 ON public.bot_vlivesubscribedchannel USING btree (group_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: kvdomingo
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: kvdomingo
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: kvdomingo
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: kvdomingo
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: alias alias_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.alias
    ADD CONSTRAINT alias_member_id_fkey FOREIGN KEY (member_id) REFERENCES public.member(id);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: bot_groupalias bot_groupalias_group_id_e557ec2e_fk_bot_group_id; Type: FK CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.bot_groupalias
    ADD CONSTRAINT bot_groupalias_group_id_e557ec2e_fk_bot_group_id FOREIGN KEY (group_id) REFERENCES public.bot_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: bot_member bot_member_group_id_1298951f_fk_bot_group_id; Type: FK CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.bot_member
    ADD CONSTRAINT bot_member_group_id_1298951f_fk_bot_group_id FOREIGN KEY (group_id) REFERENCES public.bot_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: bot_memberalias bot_memberalias_member_id_b75dc052_fk_bot_member_id; Type: FK CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.bot_memberalias
    ADD CONSTRAINT bot_memberalias_member_id_b75dc052_fk_bot_member_id FOREIGN KEY (member_id) REFERENCES public.bot_member(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: bot_twittermediasource bot_twittermediasource_member_id_b1811a24_fk_bot_member_id; Type: FK CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.bot_twittermediasource
    ADD CONSTRAINT bot_twittermediasource_member_id_b1811a24_fk_bot_member_id FOREIGN KEY (member_id) REFERENCES public.bot_member(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: bot_twittermediasubscribedchannel bot_twittermediasubs_group_id_e9c4b8a7_fk_bot_group; Type: FK CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.bot_twittermediasubscribedchannel
    ADD CONSTRAINT bot_twittermediasubs_group_id_e9c4b8a7_fk_bot_group FOREIGN KEY (group_id) REFERENCES public.bot_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: bot_vlivesubscribedchannel bot_vlivesubscribedchannel_group_id_5ac41767_fk_bot_group_id; Type: FK CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.bot_vlivesubscribedchannel
    ADD CONSTRAINT bot_vlivesubscribedchannel_group_id_5ac41767_fk_bot_group_id FOREIGN KEY (group_id) REFERENCES public.bot_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: twitterchannel channel_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.twitterchannel
    ADD CONSTRAINT channel_group_id_fkey FOREIGN KEY (group_id) REFERENCES public."group"(id);


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: member member_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.member
    ADD CONSTRAINT member_group_id_fkey FOREIGN KEY (group_id) REFERENCES public."group"(id);


--
-- Name: twitteraccount twitteraccount_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.twitteraccount
    ADD CONSTRAINT twitteraccount_member_id_fkey FOREIGN KEY (member_id) REFERENCES public.member(id);


--
-- Name: vlivechannel vlivechannel_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: kvdomingo
--

ALTER TABLE ONLY public.vlivechannel
    ADD CONSTRAINT vlivechannel_group_id_fkey FOREIGN KEY (group_id) REFERENCES public."group"(id);


--
-- Name: LANGUAGE plpgsql; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON LANGUAGE plpgsql TO kvdomingo;


--
-- PostgreSQL database dump complete
--

