-- Reset: removes schema "ecomm" with ALL its tables and data. Use to start over, then run
-- ecomm-setup.sql again (it recreates the schema and the tables).
-- Run as postgres against ecomm_db (-d ecomm_db). There is no undo.

\set ON_ERROR_STOP on

DROP SCHEMA IF EXISTS ecomm CASCADE;

\echo 'Done: schema ecomm and everything in it were dropped.'
