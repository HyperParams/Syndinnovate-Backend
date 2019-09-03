--
-- PostgreSQL database dump
--

-- Dumped from database version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)

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
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: customerdetails; Type: TABLE; Schema: public; Owner: rachit
--

CREATE TABLE public.customerdetails (
    mobilenumber character(10),
    name character varying,
    digitalscore integer,
    is_specially_abled integer
);


ALTER TABLE public.customerdetails OWNER TO rachit;

--
-- Name: reviews; Type: TABLE; Schema: public; Owner: rachit
--

CREATE TABLE public.reviews (
    id character(10),
    mobilenumber character(10),
    digitalscore integer,
    is_specially_abled integer,
    waitingtime integer,
    oncountertime integer,
    cancellations integer,
    review character varying,
    ratings integer,
    pov integer
);


ALTER TABLE public.reviews OWNER TO rachit;

--
-- Name: test; Type: TABLE; Schema: public; Owner: rachit
--

CREATE TABLE public.test (
    id integer NOT NULL,
    num integer,
    data character varying
);


ALTER TABLE public.test OWNER TO rachit;

--
-- Name: test_id_seq; Type: SEQUENCE; Schema: public; Owner: rachit
--

CREATE SEQUENCE public.test_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.test_id_seq OWNER TO rachit;

--
-- Name: test_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: rachit
--

ALTER SEQUENCE public.test_id_seq OWNED BY public.test.id;


--
-- Name: test id; Type: DEFAULT; Schema: public; Owner: rachit
--

ALTER TABLE ONLY public.test ALTER COLUMN id SET DEFAULT nextval('public.test_id_seq'::regclass);


--
-- Data for Name: customerdetails; Type: TABLE DATA; Schema: public; Owner: rachit
--

COPY public.customerdetails (mobilenumber, name, digitalscore, is_specially_abled) FROM stdin;
9821058706	rachit saksena	10	0
9996257801	prawar	7	0
\.


--
-- Data for Name: reviews; Type: TABLE DATA; Schema: public; Owner: rachit
--

COPY public.reviews (id, mobilenumber, digitalscore, is_specially_abled, waitingtime, oncountertime, cancellations, review, ratings, pov) FROM stdin;
\.


--
-- Data for Name: test; Type: TABLE DATA; Schema: public; Owner: rachit
--

COPY public.test (id, num, data) FROM stdin;
1	100	abc
\.


--
-- Name: test_id_seq; Type: SEQUENCE SET; Schema: public; Owner: rachit
--

SELECT pg_catalog.setval('public.test_id_seq', 1, true);


--
-- Name: test test_pkey; Type: CONSTRAINT; Schema: public; Owner: rachit
--

ALTER TABLE ONLY public.test
    ADD CONSTRAINT test_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

