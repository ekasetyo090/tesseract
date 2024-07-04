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

from YT_Scrapy import YtScraper
from data_construct import data_constuct

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="ticks", palette="deep")
image_path = 'https://github.com/ekasetyo090/tesseract/raw/fc58e4f8309e2eca7da51eddaa8dc1a2fea08842/main-project/resources/tesseract_6872044.png'
#logo_image = Image.open(req.get(image_path))


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
        st.image(image_path,width=50)
    with col2:
        st.title("Project Tesseract")
    st.header("Parameter")
    channel_id_input = st.text_input(label='channel ID' ,placeholder ='input channel ID here')
    if not channel_id_input:
        channel_id = '@cecilialieberia'
    else:
        channel_id = channel_id_input
    #---------------------------
    channel_basic_data = scraper_obj.scrape_channel_basic_data(channel_id)
    list_video_id = scraper_obj.scrape_playlist_item(channel_basic_data['all_video_upload_playlist_id'])
    df_video = construct_obj.construct_df(scraper_obj.scrape_video_data(list_video_id))
    df_video['defaultAudioLanguage'] = df_video['defaultAudioLanguage'].astype(str)
    channel_name = r"{}".format(channel_basic_data['channel_name'].replace(':',' : '))
    
    day_list = []
    option_dur = st.selectbox("Content By Duration",
                                    ("All", 
                                     "Short",
                                     "Long"),index=0)
    
    #df_per_dur = df_video.copy()
    if option_dur == 'Short':
        df_filter = df_video.loc[df_video["duration(s)"]<=60].copy()
    elif option_dur == 'Long':
        df_filter = df_video.loc[df_video["duration(s)"]>60].copy()
    else:
        df_filter = df_video.copy()
    df_filter.sort_values(by='hour', ascending=True,inplace=True)
    option_day = st.selectbox("Content By Day",
                                    df_filter['day'].unique(),index=0)
    df_sort_day = df_filter.loc[df_filter['df_filter']==option_day]
    option_metric = st.selectbox("Metric Type For Language",
                                    ("Likes", 
                                     "Views",
                                     "Favorite",
                                     "Comment"),index=1)
    metrics= {"Likes":'like_count',
                          "Views":'view_count',
                          "Favorite":'favorite_count',
                          "Comment":'comment_count'}
   

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
    fig, ax = plt.subplots()
    plot = sns.lineplot(data=df_sort_day,x='start_time(UTC)',
                        y=metrics.get(option_metric),
                        ax=ax)
    ax.set(xlabel='Date', 
           ylabel=option_metric, 
           title=f'Performance Over Time By Content Type And Metric {option_metric}')
    ax.grid(True)
    ax.tick_params(axis='x', which='both', labelrotation=45)

    st.pyplot(fig,use_container_width=True)
        
            
st.header('Language',divider='rainbow')

with st.container(border=None):
    if not df_video['defaultAudioLanguage'].empty:
        fig, ax = plt.subplots(figsize=(10,3))
        sns.boxplot(data=df_sort_day,
                    x=metrics.get(option_metric),
                    y='defaultAudioLanguage',showmeans=True,
                    ax=ax)
        ax.set(xlabel=option_metric, 
               ylabel='Language', 
               title='Performance By Language')
        ax.grid(True)
        st.pyplot(fig,use_container_width=True)
    else:
        st.write("Language Data Empty")
        
st.header('Days',divider='rainbow')

with st.container(border=None):
    if not df_video['day'].empty:
        fig, ax = plt.subplots()
        sns.boxplot(data=df_filter,
                    x=metrics.get(option_metric),
                    y='day',showmeans=True,
                    ax=ax)
        ax.set(xlabel=option_day, 
               ylabel='Day', 
               title='Performance By Days')
        ax.grid(True)
        st.pyplot(fig,use_container_width=True)
    else:
        st.write("Day Data Empty")
        
st.header('Hour',divider='rainbow')
with st.container(border=None):
    if not df_video['hour'].empty: 
        fig, ax = plt.subplots()
        sns.lineplot(
            data=df_sort_day, x="hour", y=metrics.get(option_metric),ax=ax)
            
        ax.set(xlabel='Hour', 
               ylabel=option_metric, 
               title='Performance By Hour (UTC)')
        ax.grid(True)
        
        st.pyplot(fig,use_container_width=True)
    else:
        st.write("Hour Data Empty")
st.header('Topic Category',divider='rainbow')
with st.container(border=None):
    if not df_video['parent_topic_primary'].empty and not df_video['parent_topic'].empty:
        option_category_type = st.selectbox("Category Type",
                                            ("Primary Category", 
                                             "Sub-Category",
                                             ),index=1)
        topic_dict = {"Primary Category":'parent_topic_primary',
                      "Sub-Category":'parent_topic'}
        fig, ax = plt.subplots()
        sns.boxplot(data=df_sort_day,
                    x=metrics.get(option_metric),
                    y=topic_dict.get(option_category_type),
                    showmeans=True,
                    ax=ax)
        ax.set(xlabel=option_metric, 
               ylabel='Category', 
               title='Performance By Category')
        ax.grid(True)
        st.pyplot(fig,use_container_width=True)
    else:
        st.write("Category Data Empty")
        
st.header('Duration',divider='rainbow')
with st.container(border=None):
    if not df_video['duration(s)'].empty: 
        fig, ax = plt.subplots()
        sns.regplot(data=df_sort_day, x="duration(s)", y=metrics.get(option_metric),
                    ax=ax,logx=True)
        ax.set(xlabel='Duration In Seconds', 
               ylabel=option_metric, 
               title=f'Relation Between {option_metric} And Duration')
        ax.grid(True)
        st.pyplot(fig,use_container_width=True)
    else:
        st.write("Duration Data Empty")
        
st.header('Licensed Content',divider='rainbow')
with st.container(border=None):
    if not df_video['licensed_content'].empty: 
        fig, ax = plt.subplots()
        sns.boxplot(data=df_sort_day,
                    x=metrics.get(option_metric),
                    y='licensed_content',
                    showmeans=True,
                    ax=ax)
        ax.set(xlabel=option_metric, 
               ylabel='Licensed Content', 
               title='Performance By Licensed Content')
        ax.grid(True)
        st.pyplot(fig,use_container_width=True)
    else:
        st.write("Licensed Data Empty")
        
st.header('For Kids',divider='rainbow')
with st.container(border=None):
    if not df_video['for_kids'].empty:
        fig, ax = plt.subplots()
        sns.boxplot(data=df_sort_day,
                    x=metrics.get(option_metric),
                    y='for_kids',
                    showmeans=True,
                    ax=ax)
        ax.set(xlabel=option_metric, 
               ylabel='For Kids', 
               title='Performance By For Kids')
        ax.grid(True)
        st.pyplot(fig,use_container_width=True)
    else:
        st.write("For Kids Data Empty")

        
   
       