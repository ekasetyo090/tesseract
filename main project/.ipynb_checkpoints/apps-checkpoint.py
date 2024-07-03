# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 16:46:04 2024

@author: snsv
"""

import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../library')))
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './resources')))

import datetime
import pandas as pd
import streamlit as st
from PIL import Image
from YT_Scrapy import YtScraper
logo_image = Image.open("resources/tesseract_6872044.png")


scraper_obj = YtScraper()
# = 'tesseract_6872044.png'
#st.set_page_config(layout="wide")
#st.set_page_config(page_title='Hololive ID 3rd Generation')
st.set_page_config(
    page_title="Youtube Miner",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded",
    
)

with st.sidebar:
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(logo_image,width=50)
    with col2:
        st.title("Project Tesseract")
    st.header("Parameter")
    channel_id_input = st.text_input(label='channel ID' ,placeholder ='input channel ID here')
    if not channel_id_input:
        channel_id = '@cecilialieberia'
    else:
        channel_id = channel_id_input

   
channel_basic_data = scraper_obj.scrape_channel_basic_data(channel_id)
list_video_id = scraper_obj.scrape_playlist_item(channel_basic_data['all_video_upload_playlist_id'])
df_video = scraper_obj.scrape_video_data(list_video_id)

channel_name = r"{}".format(channel_basic_data['channel_name'].replace(':',' : '))
col1, col2 = st.columns([1, 7])
with col1:
    st.image(channel_basic_data['thumbnails_default'],width=100)
with col2:
    st.header(channel_name)
    st.write(channel_basic_data['topic'].replace(',',', '))
st.divider()
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric(label="Subscriber", value=channel_basic_data['subs_count'])
with col2:
    st.metric(label="Views", value=channel_basic_data['views_count'])
with col3:
    st.metric(label="Video", value=channel_basic_data['video_count'])
with col4:
    st.metric(label="Family Safe", value=channel_basic_data['isFamilySafe'])
with col5:
    st.metric(label="Country", value=channel_basic_data['country'])

    
col1, col2, col3, col4, col5  = st.columns(5)
with col1:
    st.metric(label='Average Views', value=round(df_video['view_count'].mean(),1))
    
with col2:
    st.metric(label='Average Comment',value=round(df_video['comment_count'].mean(),1))
with col3:
    st.metric(label='Average Duration Video (Minutes)',value=round(df_video['duration(s)'].mean()/60,1))
with col4:
    st.metric(label='Average Likes',value=round(df_video['like_count'].mean(),1))
with col5:
    st.metric(label='Date Created',value=channel_basic_data['date_created(UTC)'].strftime('%Y-%m-%d'))
st.divider()
st.header('Metric By Video Topic')
st.write(len(df_video['topic_category'].unique()))
st.write(channel_basic_data)
st.dataframe(df_video)
        
   
       