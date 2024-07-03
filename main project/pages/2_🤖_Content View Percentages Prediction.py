# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 13:39:17 2024

@author: snsv
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.../library')))
import streamlit as st

from YT_Scrapy import YtScraper
from data_construct import data_constuct
import time
import concurrent.futures

@st.cache_data
def process_data(context):
    # Lakukan operasi yang ingin Anda jalankan secara bersamaan di sini
    # (misalnya, pemrosesan sub_topic atau primary_topic)
    processed_context = ','.join(list(set((','.join(context)).split(','))))
    return processed_context.lower()



obj_scraper = YtScraper()
obj_construct = data_constuct()

st.set_page_config(
    page_title='🤖 TSS B')
with st.spinner('Wait for it...'):
    time.sleep(5)
st.success('Model Under Development')

#with col1:
    #title = st.text_input("Content Title", '')
#with col2:                        
    #thumbnail = st.file_uploader(label='Upload Thumbnail', 
                     #type= ['png', 'jpg'], 
                     #accept_multiple_files=False, 
                     #key=None, 
                     #help=None, 
                     #on_change=None, 
                     #args=None, 
                     #disabled=False, 
                     #label_visibility="visible")
#preddict_prepare = False
#if title:
    #search_context = obj_scraper.scrape_search_video(q=title,max_data=100)
    #search_context = obj_construct.construct_df_ML(search_context)
    #search_context = search_context[['sub-topic','primary_topic']]
    #sub_topic_context, primary_topic_context = (search_context['video_topic'].dropna().to_list(), 
                                                #search_context['topic_primary'].dropna().to_list())
    #with concurrent.futures.ThreadPoolExecutor() as executor:
        #future_sub_topic = executor.submit(process_data, sub_topic_context)
        #future_primary_topic = executor.submit(process_data, primary_topic_context)
    
        #processed_sub_topic = future_sub_topic.result()
        #processed_primary_topic = future_primary_topic.result()
    #llm_input = f'''
    #title : {title} [SEP] 
    #primary topic : {processed_primary_topic} [SEP] 
    #sub topic : {processed_primary_topic}'''
    #preddict_prepare = True
    

    
if thumbnail and preddict_prepare:
    st.write(llm_input)
    st.image(thumbnail)
