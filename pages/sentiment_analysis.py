import streamlit as st
from nlp._preprocessing import web_scrape

st.dataframe(web_scrape())