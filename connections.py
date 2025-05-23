import os
import psycopg2
import logging
import streamlit as st


DB_POS_HOST = st.secrets["DB_POS_HOST"]
DB_POS_PORT = st.secrets["DB_POS_PORT"]
DB_POS_NAME = st.secrets["DB_POS_NAME"]
DB_POS_USER = st.secrets["DB_POS_USER"]
DB_POS_PASS = st.secrets["DB_POS_PASS"]

def connection_pos():
    HOST = DB_POS_HOST
    DB_NAME = DB_POS_NAME
    USER = DB_POS_USER
    PASSWORD = DB_POS_PASS
    PORT = DB_POS_PORT

    conn = psycopg2.connect(
        host=HOST,
        database=DB_NAME,
        user=USER,
        password=PASSWORD,
        port=PORT)
    return conn

def conn_string_pos():
        return f"postgresql://{DB_POS_USER}:{DB_POS_PASS}@{DB_POS_HOST}/{DB_POS_NAME}"