--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0 (Debian 17.0-1.pgdg120+1)
-- Dumped by pg_dump version 17.0

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
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS '';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: _prisma_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public._prisma_migrations (
    id character varying(36) NOT NULL,
    checksum character varying(64) NOT NULL,
    finished_at timestamp with time zone,
    migration_name character varying(255) NOT NULL,
    logs text,
    rolled_back_at timestamp with time zone,
    started_at timestamp with time zone DEFAULT now() NOT NULL,
    applied_steps_count integer DEFAULT 0 NOT NULL
);


ALTER TABLE public._prisma_migrations OWNER TO postgres;

--
-- Name: article; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.article (
    id integer NOT NULL,
    title text NOT NULL,
    content text NOT NULL,
    views integer DEFAULT 0 NOT NULL,
    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp(3) without time zone NOT NULL,
    user_id integer NOT NULL,
    likes_count integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.article OWNER TO postgres;

--
-- Name: article_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.article_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.article_id_seq OWNER TO postgres;

--
-- Name: article_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.article_id_seq OWNED BY public.article.id;


--
-- Name: category; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.category (
    id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.category OWNER TO postgres;

--
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
-- Name: category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.category_id_seq OWNED BY public.category.id;


--
-- Name: category_to_article; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.category_to_article (
    article_id integer NOT NULL,
    category_id integer NOT NULL
);


ALTER TABLE public.category_to_article OWNER TO postgres;

--
-- Name: comment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.comment (
    id integer NOT NULL,
    content text NOT NULL,
    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp(3) without time zone NOT NULL,
    article_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.comment OWNER TO postgres;

--
-- Name: comment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.comment_id_seq OWNER TO postgres;

--
-- Name: comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.comment_id_seq OWNED BY public.comment.id;


--
-- Name: file; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.file (
    id integer NOT NULL,
    path text NOT NULL,
    filename text NOT NULL,
    mimetype text NOT NULL,
    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp(3) without time zone NOT NULL,
    article_id integer NOT NULL
);


ALTER TABLE public.file OWNER TO postgres;

--
-- Name: file_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.file_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.file_id_seq OWNER TO postgres;

--
-- Name: file_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.file_id_seq OWNED BY public.file.id;


--
-- Name: like; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."like" (
    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp(3) without time zone NOT NULL,
    article_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public."like" OWNER TO postgres;

--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    email text NOT NULL,
    role text DEFAULT 'user'::text NOT NULL,
    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp(3) without time zone NOT NULL,
    hashedpassword text NOT NULL,
    username text NOT NULL
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_id_seq OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: article id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.article ALTER COLUMN id SET DEFAULT nextval('public.article_id_seq'::regclass);


--
-- Name: category id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.category ALTER COLUMN id SET DEFAULT nextval('public.category_id_seq'::regclass);


--
-- Name: comment id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comment ALTER COLUMN id SET DEFAULT nextval('public.comment_id_seq'::regclass);


--
-- Name: file id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.file ALTER COLUMN id SET DEFAULT nextval('public.file_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Data for Name: _prisma_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public._prisma_migrations (id, checksum, finished_at, migration_name, logs, rolled_back_at, started_at, applied_steps_count) FROM stdin;
179a0a16-da92-4961-b3c6-83126ab06283	625a6d2fa6b0540084a8837e1dca028e4bb9b9b75140e64942bcd762c33f8c2b	2024-11-05 10:13:50.516592+00	20241025152802_init	\N	\N	2024-11-05 10:13:50.50491+00	1
65936af8-c756-4cf3-a82e-7462eb7d376e	1411b2b4479c3633d9a2c79bbdf7a9bcdc7071ff5a95cfdaae9869638ab1aee0	2024-11-05 10:13:50.520957+00	20241027181001_add_cascade_delete_categorytoarticle	\N	\N	2024-11-05 10:13:50.517603+00	1
81ed886f-0178-420f-aed5-ff38fefca800	243fcbd364260a66582714feda61cdfc3a61d4cf5c5b7deeafc0cdb13465e02a	2024-11-05 10:13:50.536896+00	20241028125927_update_name_of_tables	\N	\N	2024-11-05 10:13:50.522553+00	1
af7b67ba-dc26-4696-9f51-e36b610bdbb0	98314490adecc155a3a31212a00620387b88149f5789db5751a7ee6f57145d85	2024-11-05 10:13:50.541422+00	20241029070406_renaming	\N	\N	2024-11-05 10:13:50.537885+00	1
86e2cc9d-c94e-44e1-b480-ffed9ba0f996	eeb7b8c5a4f771c67f1215782e7f3f10582103fd535cf24dd63811b8b9cb8882	2024-11-05 10:13:50.545043+00	20241031165342_add_cascade_delete	\N	\N	2024-11-05 10:13:50.542143+00	1
014b962c-980b-4d06-b9ae-0945ea4749f2	746483e6acbab18c2a4fb77bddf654ef785ead65c318a39be0673cda8d83e782	2024-11-05 10:13:50.94746+00	20241105101350_add_article_files_relation	\N	\N	2024-11-05 10:13:50.942834+00	1
\.


--
-- Data for Name: article; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.article (id, title, content, views, created_at, updated_at, user_id, likes_count) FROM stdin;
1	article	article 1	0	2024-11-06 04:53:30.221	2024-11-06 04:53:30.221	1	0
2	article	article 1	0	2024-11-06 04:55:04.233	2024-11-06 04:55:04.233	1	0
3	article2	article2	0	2024-11-06 04:55:38.409	2024-11-06 04:55:38.409	1	0
4	article2	article 22222	0	2024-11-06 04:57:27.693	2024-11-06 04:57:27.693	1	0
5	string3	string3	0	2024-11-06 05:12:01.477	2024-11-06 05:12:01.477	1	0
6	string4	string4	0	2024-11-06 05:19:51.367	2024-11-06 05:19:51.367	1	0
7	string5	string5	0	2024-11-06 05:20:35.95	2024-11-06 05:20:35.95	1	0
8	string6	string6	0	2024-11-06 05:20:52.123	2024-11-06 05:20:52.123	1	0
10	string7	string7	0	2024-11-06 05:22:40.543	2024-11-06 05:22:40.543	1	0
11	string8	string8	0	2024-11-06 05:23:19.545	2024-11-06 05:23:19.545	1	0
12	string9	string9	0	2024-11-06 05:24:04.439	2024-11-06 05:24:04.439	1	0
13	string10	string10	0	2024-11-06 05:25:01.79	2024-11-06 05:25:01.79	1	0
14	string11	string11	0	2024-11-06 09:46:04.247	2024-11-06 09:46:04.247	1	0
15	string12	string23	0	2024-11-06 11:14:06.822	2024-11-06 11:14:06.822	1	0
16	string13	string13	0	2024-11-06 11:21:16.851	2024-11-06 11:21:16.851	1	0
17	string14	string14	0	2024-11-06 11:21:50.716	2024-11-06 11:21:50.716	1	0
18	string15	string15	0	2024-11-06 11:48:32.685	2024-11-06 11:48:32.685	1	0
\.


--
-- Data for Name: category; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.category (id, name) FROM stdin;
1	AI
2	IT
3	CS
\.


--
-- Data for Name: category_to_article; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.category_to_article (article_id, category_id) FROM stdin;
1	3
1	2
1	1
2	3
2	2
2	1
3	2
3	1
4	2
4	1
5	2
5	1
6	2
6	1
7	3
7	2
7	1
8	2
8	1
10	3
10	2
10	1
11	2
11	1
12	2
13	3
14	2
14	1
15	3
15	2
16	3
16	2
16	1
17	2
17	1
18	1
\.


--
-- Data for Name: comment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.comment (id, content, created_at, updated_at, article_id, user_id) FROM stdin;
3	real third comment	2024-11-07 15:15:35.18	2024-11-07 15:15:35.18	5	1
2	this should not work	2024-11-07 15:15:12.624	2024-11-07 15:16:45.419	3	1
4	hello 555	2024-11-07 16:13:24.867	2024-11-07 16:22:00.09	5	2
1	moderator updated this comment	2024-11-07 13:37:31.704	2024-11-07 16:26:05.889	1	1
\.


--
-- Data for Name: file; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.file (id, path, filename, mimetype, created_at, updated_at, article_id) FROM stdin;
1	uploads/5ef8f307-4122-4894-a32f-4009aca23285.jpg	5ef8f307-4122-4894-a32f-4009aca23285.jpg	image/jpeg	2024-11-06 05:19:51.387	2024-11-06 05:19:51.387	6
3	uploads/827a9f7f-fccb-47ae-9489-fb7c1174f1ad.jpg	827a9f7f-fccb-47ae-9489-fb7c1174f1ad.jpg	image/jpeg	2024-11-06 05:22:40.555	2024-11-06 05:22:40.555	10
4	uploads/21510bcd-8425-47e0-92df-b13fb76d1b56.jpg	21510bcd-8425-47e0-92df-b13fb76d1b56.jpg	image/jpeg	2024-11-06 05:23:19.553	2024-11-06 05:23:19.553	11
5	uploads/916b7d8a-3a8c-4973-bf66-197fe70e80bd.jpg	916b7d8a-3a8c-4973-bf66-197fe70e80bd.jpg	image/jpeg	2024-11-06 05:23:19.557	2024-11-06 05:23:19.557	11
6	uploads/70c2a421-fbd3-40c5-8076-0964c20e2991.jpg	70c2a421-fbd3-40c5-8076-0964c20e2991.jpg	image/jpeg	2024-11-06 05:24:04.448	2024-11-06 05:24:04.448	12
8	uploads/e4c30824-e0ce-4445-9ff2-92df2a2a275c.jpg	e4c30824-e0ce-4445-9ff2-92df2a2a275c.jpg	image/jpeg	2024-11-06 09:46:04.267	2024-11-06 09:46:04.267	14
9	uploads/e72a6583-3ec6-4475-b67a-75412ac2f351.jpg	e72a6583-3ec6-4475-b67a-75412ac2f351.jpg	image/jpeg	2024-11-06 11:14:06.842	2024-11-06 11:14:06.842	15
10	uploads/4a5e8edc-1be0-4733-a905-012c4634a889.jpg	4a5e8edc-1be0-4733-a905-012c4634a889.jpg	image/jpeg	2024-11-06 11:21:16.871	2024-11-06 11:21:16.871	16
11	uploads/de0b1d8f-13ee-4373-a519-d9968cf17493.jpg	de0b1d8f-13ee-4373-a519-d9968cf17493.jpg	image/jpeg	2024-11-06 11:21:50.727	2024-11-06 11:21:50.727	17
12	uploads/4b5735ce-31dc-4104-b791-3574af8153c8.jpg	4b5735ce-31dc-4104-b791-3574af8153c8.jpg	image/jpeg	2024-11-06 11:21:50.73	2024-11-06 11:21:50.73	17
13	uploads/91a73696-583e-436b-88e6-52eadfb1c005.jpg	91a73696-583e-436b-88e6-52eadfb1c005.jpg	image/jpeg	2024-11-06 11:48:32.701	2024-11-06 11:48:32.701	18
14	uploads/a36d34bb-9b4f-411a-bd26-f30587a443e0.jpg	a36d34bb-9b4f-411a-bd26-f30587a443e0.jpg	image/jpeg	2024-11-06 11:49:09.857	2024-11-06 11:49:09.857	4
15	uploads/35a551ee-3c0f-4ddc-982a-d8dde96bde29.jpg	35a551ee-3c0f-4ddc-982a-d8dde96bde29.jpg	image/jpeg	2024-11-06 12:05:12.074	2024-11-06 12:05:12.074	4
16	uploads/7cb93376-eead-4c69-80eb-ad146c07b4d5.jpg	7cb93376-eead-4c69-80eb-ad146c07b4d5.jpg	image/jpeg	2024-11-06 12:17:19.974	2024-11-06 12:17:19.974	4
17	uploads/8a21c621-76bf-4f51-9012-d927a45d2770.jpg	8a21c621-76bf-4f51-9012-d927a45d2770.jpg	image/jpeg	2024-11-08 09:51:23.385	2024-11-08 09:51:23.385	2
\.


--
-- Data for Name: like; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."like" (created_at, updated_at, article_id, user_id) FROM stdin;
2024-11-08 09:50:46.532	2024-11-08 09:50:46.532	14	2
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, email, role, created_at, updated_at, hashedpassword, username) FROM stdin;
2	name2@gmail.com	user	2024-11-05 10:16:09.421	2024-11-05 10:16:09.421	$2b$12$ueLXne.ZkbUyzPLxlg2ehebxBbSO/9.KQwcYTbEXexpfIvDAN1Bba	name2
3	admin@example.com	admin	2024-11-07 08:59:19.58	2024-11-07 08:59:19.586	$2b$12$JCc0/rjnErTy99./PwZ9l.b0zbZQLoEK6/myJQH1g53m5aG2J/1Ra	admin
4	moderator@example.com	moderator	2024-11-07 09:02:02.341	2024-11-07 09:02:02.35	$2b$12$BvQEmRShMuxD/nVQqYNECO8ufID863AInwuQ00FghSsLQ8ADGvVLa	moderator
5	moderator2@example.com	moderator	2024-11-07 09:03:04.138	2024-11-07 09:03:04.145	$2b$12$BVa2Z7XUWdwgOVdYraD8WeIv5t3lkGpvUPiuiVUXWye0b0PU3Qf9q	moderator2
1	name1@gmail.com	author	2024-11-05 10:15:44.403	2024-11-07 09:16:38.456	$2b$12$R52I5wyAGYs7j5x5UmuaDuakcu4fQm733R/Gmxlhv6p86w8rYT/My	name1
\.


--
-- Name: article_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.article_id_seq', 18, true);


--
-- Name: category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.category_id_seq', 3, true);


--
-- Name: comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.comment_id_seq', 4, true);


--
-- Name: file_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.file_id_seq', 17, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 5, true);


--
-- Name: _prisma_migrations _prisma_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public._prisma_migrations
    ADD CONSTRAINT _prisma_migrations_pkey PRIMARY KEY (id);


--
-- Name: article article_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.article
    ADD CONSTRAINT article_pkey PRIMARY KEY (id);


--
-- Name: category category_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.category
    ADD CONSTRAINT category_pkey PRIMARY KEY (id);


--
-- Name: category_to_article category_to_article_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.category_to_article
    ADD CONSTRAINT category_to_article_pkey PRIMARY KEY (article_id, category_id);


--
-- Name: comment comment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT comment_pkey PRIMARY KEY (id);


--
-- Name: file file_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.file
    ADD CONSTRAINT file_pkey PRIMARY KEY (id);


--
-- Name: like like_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."like"
    ADD CONSTRAINT like_pkey PRIMARY KEY (article_id, user_id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user_email_key; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX user_email_key ON public."user" USING btree (email);


--
-- Name: article article_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.article
    ADD CONSTRAINT article_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: category_to_article category_to_article_article_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.category_to_article
    ADD CONSTRAINT category_to_article_article_id_fkey FOREIGN KEY (article_id) REFERENCES public.article(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: category_to_article category_to_article_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.category_to_article
    ADD CONSTRAINT category_to_article_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.category(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: comment comment_article_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT comment_article_id_fkey FOREIGN KEY (article_id) REFERENCES public.article(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: comment comment_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT comment_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: file file_article_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.file
    ADD CONSTRAINT file_article_id_fkey FOREIGN KEY (article_id) REFERENCES public.article(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: like like_article_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."like"
    ADD CONSTRAINT like_article_id_fkey FOREIGN KEY (article_id) REFERENCES public.article(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: like like_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."like"
    ADD CONSTRAINT like_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;


--
-- PostgreSQL database dump complete
--

