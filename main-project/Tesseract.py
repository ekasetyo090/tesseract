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
from datetime import timedelta

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import seaborn as sns
import pandas as pd
sns.set_theme(style="ticks", palette="deep")
image_path = 'https://github.com/ekasetyo090/tesseract/raw/fc58e4f8309e2eca7da51eddaa8dc1a2fea08842/main-project/resources/tesseract_6872044.png'
#logo_image = Image.open(req.get(image_path))

@st.cache_data
def get_start_of_week(date):
  day_offset = date.weekday()
  return date - timedelta(days=day_offset)


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
    st.subheader("Channel ID")
    channel_id_input = st.text_input(label='channel ID' ,placeholder ='input channel ID here')
    if not channel_id_input:
        channel_id = '@cecilialieberia'
    else:
        channel_id = channel_id_input
    st.subheader("Metric")
    option_metric = st.selectbox("Metric Type",
                                    ("Likes", 
                                     "Views",
                                     "Favorite",
                                     "Comment"),index=1)
    
    #---------------------------
    channel_basic_data = scraper_obj.scrape_channel_basic_data(channel_id)
    list_video_id = scraper_obj.scrape_playlist_item(channel_basic_data['all_video_upload_playlist_id'])
    df_video = construct_obj.construct_df(scraper_obj.scrape_video_data(list_video_id))
    df_video['defaultAudioLanguage'] = df_video['defaultAudioLanguage'].astype(str)
    # Assuming df_video is already defined
    df_video['start_time(UTC)'] = pd.to_datetime(df_video['start_time(UTC)'])

    df_video['video_lenght'] = df_video['duration(s)'].apply(lambda x: 'Short' if x<=60 else 'Long')
    channel_name = r"{}".format(channel_basic_data['channel_name'].replace(':',' : '))
    #df_video['is_live'] = df_video['']
    
    st.subheader("Filter")
    
    #df_filter.sort_values(by='hour', ascending=True,inplace=True)
    #list_day_filter = df_filter['day'].unique().tolist()
    
    metrics= {"Likes":'like_count',
                          "Views":'view_count',
                          "Favorite":'favorite_count',
                          "Comment":'comment_count'}
    
    start_date, end_date = st.date_input(
        label='Date Range',min_value=df_video['start_time(UTC)'].min(),
        max_value=df_video['start_time(UTC)'].max(),
        value=[
            df_video['start_time(UTC)'].min(), 
            df_video['start_time(UTC)'].max()
            ]
    )
    df_video = df_video.loc[(df_video['start_time(UTC)'] <= str(end_date)) & (df_video['start_time(UTC)'] >= str(start_date))] 
   
   

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

col1, col2 = st.columns(2)
df_performance = df_video.copy()
with col1:
    st.header('Performance',divider='rainbow')
    subcol1,subcol2,subcol3 = st.columns(3)
    with subcol1:
        date_trunc_permformance = st.selectbox("Performance Date Truncate",("None",
                                                                            "Weekly",
                                                                            "Monthly"),
                                               index=0)
        
        hue_perform_menu = {'None':["None","Day name","Main category",
                                    "Language","Duration",'Licence','For kids'],
                            'Day':["None","Main category","Language",
                                   "Duration",'Licence','For kids'],
                            'Language':["None","Day name","Main category",
                                        "Duration",'Licence','For kids'],
                            'Duration':["None","Day name","Main category",
                                        "Language",'Licence','For kids'],
                            'Licence':["None","Day name","Main category",
                                       "Language","Duration",'For kids'],
                            'For kids':["None","Day name","Main category",
                                        "Language","Duration",'Licence'],
                            'Main category':["None","Day name","Language",
                                             "Duration",'Licence','For kids']}
        perform_filter_dict = {
                'Day':'day','Language':'defaultAudioLanguage',
                'Duration':'video_lenght','Licence':'licensed_content',
                'For kids':'for_kids','Main category':'parent_topic_primary'
                }
       
        
    with subcol2:
        perform_filter = st.selectbox("Performance Filter",
                                      ("None","Day","Language",
                                       "Duration",'Licence','For kids','Main category'),
                                      index=0)
        if perform_filter != 'None':
            perform_filter_menu = df_video[perform_filter_dict.get(perform_filter)].unique().tolist()
            perform_filter_input = st.selectbox("Performance filter by",
                                                (perform_filter_menu),
                                                index=0)
            df_performance = df_performance.loc[df_performance[perform_filter_dict.get(perform_filter)] == perform_filter_input]
        
        
    
    with subcol3:
        hue_permformance = st.selectbox("Performance Hue",
                                        (hue_perform_menu.get(perform_filter)),
                                        index=0
                                        )
        
    
    
    if date_trunc_permformance != 'None':
        if date_trunc_permformance == 'Weekly':
            df_performance['date_trunc'] = df_performance['start_time(UTC)'].apply(get_start_of_week)
            #get_start_of_week
            
        elif date_trunc_permformance == 'Monthly':
            df_performance['date_trunc'] = df_performance['start_time(UTC)'].apply(lambda x: x.strftime('%Y-%m'))
    else:
        df_performance['date_trunc'] = df_performance['start_time(UTC)']
    df_performance.sort_values(by='date_trunc',ascending=True,inplace=True)
    
    
    
   
        
    
    fig,ax = plt.subplots(figsize=(7,4))
    sns.lineplot(data=df_performance,
                 y=metrics.get(option_metric),
                 x='date_trunc',
                 hue=perform_filter_dict.get(hue_permformance),
                 ax=ax
                 )
    
    ax.set_title(f"Performance (by date) with hue {hue_permformance}")
    ax.set_xlabel("Date")
    ax.set_ylabel(f"{option_metric} Count")
    plt.xticks(rotation=45, ha='right')
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.grid(True)
    st.pyplot(fig=fig, clear_figure=None, use_container_width=True, )
        
with col2:
    st.header('Hour',divider='rainbow')
    df_hour = df_video.copy()
    df_hour.sort_values(by='hour',ascending=True,inplace=True)
    subcol1,subcol2= st.columns(2)
    with subcol1:
        hour_filter = st.selectbox(
            "Hour Filter",
            ("None","Day",
             "Language","Duration",'Licence',
             'For kids',
             'Main category'
             ),
            index=0)
        hour_filter_dict = {
            'Day':'day','Language':'defaultAudioLanguage',
            'Duration':'video_lenght','Licence':'licensed_content',
            'For kids':'for_kids','Main category':'parent_topic_primary'
            }
        if hour_filter != 'None':
            col_hour = hour_filter_dict.get(hour_filter)
            list_val_filter = df_hour[col_hour].unique().tolist()
            hour_filter_box = st.selectbox("Hour filter value",list_val_filter,index=0)
        hue_hour_menu = {'None':["None","Day name","Main category",
                                 "Language","Duration",'Licence','For kids'],
                         'Day':["None","Main category","Language",
                                "Duration",'Licence','For kids'],
                         'Language':["None","Day name","Main category",
                                     "Duration",'Licence','For kids'],
                         'Duration':["None","Day name","Main category",
                                     "Language",'Licence','For kids'],
                         'Licence':["None","Day name","Main category",
                                    "Language","Duration",'For kids'],
                         'For kids':["None","Day name","Main category",
                                     "Language","Duration",'Licence'],
                         'Main category':["None","Day name","Language",
                                          "Duration",'Licence','For kids']}
            
    with subcol2:
        hue_hour = st.selectbox("Hour Hue",
                                (hue_hour_menu.get(hour_filter)),
                                index=0)
        hour_dict = {'Day name':'day','Main category':'parent_topic_primary',
                     'Language':'defaultAudioLanguage','Duration':'video_lenght',
                     'None':None,'Licence':'licensed_content',
                     'For kids':'for_kids','Main category':'parent_topic_primary'}
        if hour_filter != 'None':
            df_hour = df_hour.loc[df_hour[col_hour]==hour_filter_box]
    
    fig,ax = plt.subplots(figsize=(7,4))
    sns.lineplot(data=df_hour,
                 y=metrics.get(option_metric),
                 x='hour',
                 hue=hour_dict.get(hue_hour),
                 ax=ax)
    ax.set_title(f"Hour with hue {hue_permformance}")
    ax.set_xlabel("Hour")
    ax.set_ylabel(f"{option_metric} Count")
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    st.pyplot(fig=fig, clear_figure=None, use_container_width=True)

with st.container(height=None, border=None):
    df_cat = df_video.copy()
    st.header("Category",divider='rainbow')
    col1, col2 = st.columns([1,5])
    with col1:
        
        
        cat_plot_type = st.selectbox("Category type",
                                ('Main category','Sub category'),
                                index=0)
        cat_plot_type_dict = {'Main category':'parent_topic_primary',
                              'Sub category':'parent_topic'}
    
        cat_plot_hue = st.selectbox(
            "Category hue",
            ('None','Day','Duration','Language','Licence','For kids'),
            index=0)
        cat_plot_hue_dict = {'None':None,
                             'Day':'day',
                             'Duration':'video_lenght',
                             'Language':'defaultAudioLanguage',
                             'Licence':'licensed_content',
                             'For kids':'for_kids'}
    with col2:
        fig,ax = plt.subplots()
        sns.boxplot(data=df_cat,
                     y=cat_plot_type_dict.get(cat_plot_type),
                     x=metrics.get(option_metric),
                     hue=cat_plot_hue_dict.get(cat_plot_hue),
                     ax=ax,
                     showmeans=True )
        ax.set_xlabel(f"{option_metric} Count")
        ax.set_ylabel(cat_plot_type)
        plt.grid(True)
        st.pyplot(fig=fig, clear_figure=None, use_container_width=True, )
#st.dataframe(df_video)
  
       