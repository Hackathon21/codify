import streamlit as st
from PIL import Image
import pandas as pd
import base64
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import json

import yfinance as yf
import pandas as pd
import cufflinks as cf
import datetime
import numpy as np

# mail ..........
from bs4 import BeautifulSoup
import requests
import time
import smtplib
import ssl
from email.mime.text import MIMEText as MT
from email.mime.multipart import MIMEMultipart as MM

st.set_page_config(layout="wide")

LOGO_IMAGE = "logo2.gif"

st.markdown(
    """
    <style>
    .container {
        display: flex;
        align-items: center;
    }
    .block-container{
        padding-top: 20px;
    }
    .logo-text {
        font-weight:700 !important;
        font-size:50px !important;
        # color: #f9a01b !important;
        # padding-top: 0px !important;
        align-items: center;
    }
    .logo-img {
        float:right;
        width : 10%;
        height :20%;
        padding-right: 10px;
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


@st.cache
def load_data():
    cmc = requests.get('https://coinmarketcap.com')
    soup = BeautifulSoup(cmc.content, 'html.parser')

    data = soup.find('script', id='__NEXT_DATA__', type='application/json')
    coins = {}
    coin_data = json.loads(data.contents[0])
    listings = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']
    for i in listings:
      coins[str(i['id'])] = i['slug']

    coin_name = []
    coin_symbol = []
    market_cap = []
    percent_change_1h = []
    percent_change_24h = []
    percent_change_7d = []
    price = []
    volume_24h = []

    for i in listings:
      coin_name.append(i['slug'])
      coin_symbol.append(i['symbol'])
      price.append(i['quote'][currency_price_unit]['price'])
      percent_change_1h.append(i['quote'][currency_price_unit]['percentChange1h']) # percent_change_1h
      percent_change_24h.append(i['quote'][currency_price_unit]['percentChange24h']) #percent_change_24h
      percent_change_7d.append(i['quote'][currency_price_unit]['percentChange7d']) # percent_change_7d
      market_cap.append(i['quote'][currency_price_unit]['marketCap']) # market_cap
      volume_24h.append(i['quote'][currency_price_unit]['volume24h']) # volume_24h

    df = pd.DataFrame(columns=['coin_name', 'coin_symbol', 'marketCap', 'percentChange1h', 'percentChange24h', 'percentChange7d', 'price', 'volume24h'])
    df['coin_name'] = coin_name
    df['coin_symbol'] = coin_symbol
    df['price'] = price
    df['percentChange1h'] = percent_change_1h
    df['percentChange24h'] = percent_change_24h
    df['percentChange7d'] = percent_change_7d
    df['marketCap'] = market_cap
    df['volume24h'] = volume_24h
    return df

df = load_data()

sorted_coin = sorted( df['coin_symbol'] )
selected_coin = col1.multiselect('Cryptocurrency', sorted_coin, sorted_coin)

df_selected_coin = df[ (df['coin_symbol'].isin(selected_coin)) ] # Filtering data

num_coin = col1.slider('Display Top N Coins', 1, 100, 100)
df_coins = df_selected_coin[:num_coin]

percent_timeframe = col1.selectbox('Percent change time frame',
                                    ['7d','24h', '1h'])
percent_dict = {"7d":'percentChange7d',"24h":'percentChange24h',"1h":'percentChange1h'}
selected_percent_timeframe = percent_dict[percent_timeframe]

sort_values = col1.selectbox('Sort values?', ['Yes', 'No'])

col1.subheader('Price Data of Selected Cryptocurrency')
col1.write('Data Dimension: ' + str(df_selected_coin.shape[0]) + ' rows and ' + str(df_selected_coin.shape[1]) + ' columns.')

col1.dataframe(df_coins)

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
    return href

col1.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)

col1.subheader('Table of % Price Change')
df_change = pd.concat([df_coins.coin_symbol, df_coins.percentChange1h, df_coins.percentChange24h, df_coins.percentChange7d], axis=1)
df_change = df_change.set_index('coin_symbol')
df_change['positive_percent_change_1h'] = df_change['percentChange1h'] > 0
df_change['positive_percent_change_24h'] = df_change['percentChange24h'] > 0
df_change['positive_percent_change_7d'] = df_change['percentChange7d'] > 0
col1.dataframe(df_change)

col2.subheader('Bar plot of % Price Change')

if percent_timeframe == '7d':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percentChange7d'])
    col2.write('*7 days period*')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['percentChange7d'].plot(kind='barh', color=df_change.positive_percent_change_7d.map({True: 'g', False: 'r'}))
    col2.pyplot(plt)
elif percent_timeframe == '24h':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percentChange24h'])
    col2.write('*24 hour period*')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['percentChange24h'].plot(kind='barh', color=df_change.positive_percent_change_24h.map({True: 'g', False: 'r'}))
    col2.pyplot(plt)
else:
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percentChange1h'])
    col2.write('*1 hour period*')
    plt.figure(figsize=(5,25))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['percentChange1h'].plot(kind='barh', color=df_change.positive_percent_change_1h.map({True: 'g', False: 'r'}))
    col2.pyplot(plt)
