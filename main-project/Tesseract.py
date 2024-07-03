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
from data_construct import data_constuct

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="ticks", palette="deep")
image_path = 'https://github.com/ekasetyo090/tesseract/blob/fc58e4f8309e2eca7da51eddaa8dc1a2fea08842/main-project/resources/tesseract_6872044.png'
logo_image = Image.open(image_path)


scraper_obj = YtScraper()
construct_obj = data_constuct()
# = 'tesseract_6872044.png'
#st.set_page_config(layout="wide")
#st.set_page_config(page_title='Hololive ID 3rd Generation')
st.set_page_config(
    page_title="Youtube Digester",
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
df_video = construct_obj.construct_df(scraper_obj.scrape_video_data(list_video_id))

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


metrics= {"Likes":'like_count',
                      "Views":'view_count',
                      "Favorite":'favorite_count',
                      "Comment":'comment_count'}
st.header('Performance',divider='rainbow')

with st.container(border=None):
    col1, col2, = st.columns([1.5,5])
    with col1:
        
        option_lineplot_Performance_metric = st.selectbox("Metric Type For Performance",
                                                         ("Likes", 
                                                          "Views",
                                                          "Favorite",
                                                          "Comment"),index=0)
    with col2:
       
        fig, ax = plt.subplots()
        plot = sns.lineplot(data=df_video,x='start_time(UTC)',
                            y=metrics.get(option_lineplot_Performance_metric),
                            ax=ax)
        ax.set(xlabel='Date', 
               ylabel=option_lineplot_Performance_metric, 
               title=f'Performance Over Time By Content Type And Metric {option_lineplot_Performance_metric}')
        ax.grid(True)
        ax.tick_params(axis='x', which='both', labelrotation=45)

        st.pyplot(fig,use_container_width=True)
        
            
st.header('Language',divider='rainbow')

with st.container(border=None):
    col1, col2, = st.columns([1.5,5])
    with col1:
        option_language = st.selectbox("Metric Type For Language",
                                        ("Likes", 
                                         "Views",
                                         "Favorite",
                                         "Comment"),index=0)
    with col2:
        fig, ax = plt.subplots(figsize=(10,3))
        sns.boxplot(data=df_video,
                    x=metrics.get(option_language),
                    y='defaultAudioLanguage',showmeans=True,
                    ax=ax)
        ax.set(xlabel=option_language, 
               ylabel='Language', 
               title='Performance By Language')
        ax.grid(True)
        st.pyplot(fig,use_container_width=True)
        
st.header('Days',divider='rainbow')

with st.container(border=None):
    col1, col2, = st.columns([1.5,5])
    with col1:
        option_day = st.selectbox("Metric Type For Days",
                                        ("Likes", 
                                         "Views",
                                         "Favorite",
                                         "Comment"),index=0)
    with col2:
        fig, ax = plt.subplots()
        sns.boxplot(data=df_video,
                    x=metrics.get(option_day),
                    y='day',showmeans=True,
                    ax=ax)
        ax.set(xlabel=option_day, 
               ylabel='Day', 
               title='Performance By Days')
        ax.grid(True)
        st.pyplot(fig,use_container_width=True)
        
st.header('Hour',divider='rainbow')
with st.container(border=None):
    col1, col2, = st.columns([1.5,5])
    with col1:
        
        option_hour = st.selectbox("Metric Type For Hour",
                                        ("Likes", 
                                         "Views",
                                         "Favorite",
                                         "Comment"),index=0)
    with col2:
        fig, ax = plt.subplots()
        sns.lineplot(
            data=df_video, x="hour", y=metrics.get(option_hour),ax=ax)
            
        ax.set(xlabel='Hour', 
               ylabel=option_hour, 
               title='Performance By Hour (UTC)')
        ax.grid(True)
        
        st.pyplot(fig,use_container_width=True)
        
st.header('Topic Category',divider='rainbow')
with st.container(border=None):
    col1, col2, = st.columns([1.5,5])
    with col1:
        option_category_type = st.selectbox("Category Type",
                                            ("Primary Category", 
                                             "Sub-Category",
                                             ),index=1)
        option_category = st.selectbox("Metric Type For Category",
                                        ("Likes", 
                                         "Views",
                                         "Favorite",
                                         "Comment"),index=0)
        topic_dict = {"Primary Category":'parent_topic_primary',
                      "Sub-Category":'parent_topic'}
    with col2:
        fig, ax = plt.subplots()
        sns.boxplot(data=df_video,
                    x=metrics.get(option_day),
                    y=topic_dict.get(option_category_type),
                    showmeans=True,
                    ax=ax)
        ax.set(xlabel=option_category, 
               ylabel='Category', 
               title='Performance By Category')
        ax.grid(True)
        st.pyplot(fig,use_container_width=True)

st.header('Duration',divider='rainbow')
with st.container(border=None):
    col1, col2, = st.columns([1.5,5])
    with col1:
        option_duration = st.selectbox("Metric Type For Duration",
                                        ("Likes", 
                                         "Views",
                                         "Favorite",
                                         "Comment"),index=0)
    with col2:
        fig, ax = plt.subplots()
        sns.regplot(data=df_video, x="duration(s)", y=metrics.get(option_duration),
                    ax=ax,logx=True)
        ax.set(xlabel='Duration In Seconds', 
               ylabel=option_duration, 
               title=f'Relation Between {option_duration} And Duration')
        ax.grid(True)
        st.pyplot(fig,use_container_width=True)

st.header('Licensed Content',divider='rainbow')
with st.container(border=None):
    col1, col2, = st.columns([1.5,5])
    with col1:
        option_licensed = st.selectbox("Metric Type For Licensed Content",
                                        ("Likes", 
                                         "Views",
                                         "Favorite",
                                         "Comment"),index=0)
    with col2:
        fig, ax = plt.subplots()
        sns.boxplot(data=df_video,
                    x=metrics.get(option_licensed),
                    y='licensed_content',
                    showmeans=True,
                    ax=ax)
        ax.set(xlabel=option_licensed, 
               ylabel='Licensed Content', 
               title='Performance By Licensed Content')
        ax.grid(True)
        st.pyplot(fig,use_container_width=True)
        
st.header('For Kids',divider='rainbow')
with st.container(border=None):
    col1, col2, = st.columns([1.5,5])
    with col1:
        option_for_kids= st.selectbox("Metric Type For Kids Content",
                                        ("Likes", 
                                         "Views",
                                         "Favorite",
                                         "Comment"),index=0)
    with col2:
        fig, ax = plt.subplots()
        sns.boxplot(data=df_video,
                    x=metrics.get(option_for_kids),
                    y='for_kids',
                    showmeans=True,
                    ax=ax)
        ax.set(xlabel=option_for_kids, 
               ylabel='For Kids', 
               title='Performance By For Kids')
        ax.grid(True)
        st.pyplot(fig,use_container_width=True)
st.write(df_video.dtypes)
st.dataframe(df_video)
        
   
       