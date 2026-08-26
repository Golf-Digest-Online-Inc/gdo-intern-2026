--
-- PostgreSQL database dump
--

\restrict KlI0ordFZYdLZ2bNoWCXiZTBAlAeB4tjDpm8XV841SBrjDXlX446SVcjtoKxt62

-- Dumped from database version 18.3 (Debian 18.3-1.pgdg13+1)
-- Dumped by pg_dump version 18.3 (Debian 18.3-1.pgdg13+1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: items; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.items (
    id integer NOT NULL,
    name character varying,
    stock integer DEFAULT 0 NOT NULL,
    image character varying
);


--
-- Name: items_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.items_id_seq OWNED BY public.items.id;


--
-- Name: items id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.items ALTER COLUMN id SET DEFAULT nextval('public.items_id_seq'::regclass);


--
-- Data for Name: items; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.items VALUES (2, 'ドライバー', 0, 'images/01_doraiba-.png');
INSERT INTO public.items VALUES (1, 'キャディバッグ', 0, 'images/kyadi.png');
INSERT INTO public.items VALUES (3, 'アイアン', 0, 'images/aian.png');
INSERT INTO public.items VALUES (6, 'クーラーボックス', 1, 'images/coolerbox.png');
INSERT INTO public.items VALUES (8, 'ゴルフシューズ', 0, 'images/kutu.png');
INSERT INTO public.items VALUES (9, 'サンバイザー', 10, 'images/sun.png');
INSERT INTO public.items VALUES (10, 'ベルト', 7, 'images/beruto.png');
INSERT INTO public.items VALUES (11, 'キャップ', 1, 'images/cap.png');
INSERT INTO public.items VALUES (12, 'サングラス', 4, 'images/sunglass.png');
INSERT INTO public.items VALUES (13, 'ゴルフティー', 0, 'images/golftea.png');
INSERT INTO public.items VALUES (14, 'タオル', 6, 'images/taoru.png');
INSERT INTO public.items VALUES (15, 'クラブセット', 7, 'images/clubset.png');
INSERT INTO public.items VALUES (5, 'パター', 6, 'images/pata-.png');
INSERT INTO public.items VALUES (7, 'ドリンクボトル', 4, 'images/drink.png');
INSERT INTO public.items VALUES (4, 'ボール', 3, 'images/boll.png');


--
-- Name: items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.items_id_seq', 15, true);


--
-- Name: items items_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_pk PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

\unrestrict KlI0ordFZYdLZ2bNoWCXiZTBAlAeB4tjDpm8XV841SBrjDXlX446SVcjtoKxt62

