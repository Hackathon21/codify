import streamlit as st
from PIL import Image
import pandas as pd
import base64
import matplotlib.pyplot as plt
st.set_page_config(layout="wide")
# from bs4 import BeautifulSoup
# import requests
# import json

LOGO_IMAGE = "logo2.gif"

st.markdown(
    """
    <style>
    .container {
        display: flex;
        align-items: center;
    }
    .logo-text {
        font-weight:700 !important;
        font-size:50px !important;
        # color: #f9a01b !important;
        # padding-top: 0px !important;
        padding-left: 10px;
        align-items: center;
    }
    .logo-img {
        float:right;
        padding: 0;
        width : 10%;
        height :20%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="container">
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
        <p class="logo-text">नMASTE CRYPटो</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
This app retrieves cryptocurrency prices for the top 100 cryptocurrency from the **CoinMarketCap**!

""")
expander_bar = st.beta_expander("About")
expander_bar.markdown("""
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn, BeautifulSoup, requests, json, time
* **Data source:** [CoinMarketCap](http://coinmarketcap.com).
""")
col1, col2 = st.beta_columns((1,1))
col1.header('Input Options')
currency_price_unit = col1.selectbox('Select currency for price', ('USD', 'BTC', 'ETH'))
