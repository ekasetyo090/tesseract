#import pandas as pd
class data_constuct:
    def __init__(self):
        self.PARRENT_TOPIC = {'Christian music':'Music',
                                 'Classical music':'Music',
                                 'Country':'Music',
                                 'Electronic music':'Music',
                                 'Hip hop music':'Music',
                                 'Independent music':'Music',
                                 'Jazz':'Music',
                                 'Music of Asia':'Music',
                                 'Music of Latin America':'Music',
                                 'Pop music':'Music',
                                 'Reggae':'Music',
                                 'Rhythm and blues':'Music',
                                 'Rock music':'Music',
                                 'Soul music':'Music',
                                 'Music':'Music',
                                 'Gaming':'Gaming',
                                 'Action game':'Gaming',
                                 'Action adventure game':'Gaming',
                                 'Casual game':'Gaming',
                                 'Music video game':'Gaming',
                                 'Puzzle video game':'Gaming',
                                 'Racing video game':'Gaming',
                                 'Role playing video game':'Gaming',
                                 'Simulation video game':'Gaming',
                                 'Sports game':'Gaming',
                                 'Strategy video game':'Gaming',
                                 'Video game culture':'Gaming',
                                 'Sports':'Sports',
                                 'American football':'Sports',
                                 'Baseball':'Sports',
                                 'Basketball':'Sports',
                                 'Boxing':'Sports',
                                 'Cricket':'Sports',
                                 'Football':'Sports',
                                 'Golf':'Sports',
                                 'Ice hockey':'Sports',
                                 'Mixed martial arts':'Sports',
                                 'Motorsport':'Sports',
                                 'Tennis':'Sports',
                                 'Volleyball':'Sports',
                                 'Entertainment':'Entertainment',
                                 'Humor':'Entertainment',
                                 'Movies':'Entertainment',
                                 'Performing arts':'Entertainment',
                                 'Professional wrestling':'Entertainment',
                                 'TV shows':'Entertainment',
                                 'Lifestyle':'Lifestyle',
                                 'Fashion':'Lifestyle',
                                 'Fitness':'Lifestyle',
                                 'Food':'Lifestyle',
                                 'Hobby':'Lifestyle',
                                 'Pets':'Lifestyle',
                                 'Physical attractiveness [Beauty]':'Lifestyle',
                                 'Technology':'Lifestyle',
                                 'Tourism':'Lifestyle',
                                 'Vehicles':'Lifestyle',
                                 'Lifestyle (sociology)':'Lifestyle',
                                 'Society':'Society',
                                 'Business':'Society',
                                 'Health':'Society',
                                 'Military':'Society',
                                 'Politics':'Society',
                                 'Religion':'Society',
                                 'Knowledge':'Knowledge',
                                }
        self.PARENT_TOPIC_ID = {'2' : 'Autos & Vehicles',
                                '1' :  'Film & Animation',
                                '10' : 'Music',
                                '15' : 'Pets & Animals',
                                '17' : 'Sports',
                                '18' : 'Short Movies',
                                '19' : 'Travel & Events',
                                '20' : 'Gaming',
                                '21' : 'Videoblogging',
                                '22' : 'People & Blogs',
                                '23' : 'Comedy',
                                '24' : 'Entertainment',
                                '25' : 'News & Politics',
                                '26' : 'How to & Style',
                                '27' : 'Education',
                                '28' : 'Science & Technology',
                                '29' : 'Nonprofits & Activism',
                                '30' : 'Movies',
                                '31' : 'Anime/Animation',
                                '32' : 'Action/Adventure',
                                '33' : 'Classics',
                                '34' : 'Comedy',
                                '35' : 'Documentary',
                                '36' : 'Drama',
                                '37' : 'Family',
                                '38' : 'Foreign',
                                '39' : 'Horror',
                                '40' : 'Sci-Fi/Fantasy',
                                '41' : 'Thriller',
                                '42' : 'Shorts',
                                '43' : 'Shows',
                                '44' : 'Trailers',
                            }
    def parent_topic_id(self,x):
        id = self.PARENT_TOPIC_ID.get(x)
        if id:
            return id
        else:
            return 'Other'
    def parent_topic(self,x):
        temp_list = []
        x = x.split(',')
        for i in x:
            if i in self.PARRENT_TOPIC.keys():
                temp_list.append(self.PARRENT_TOPIC.get(i))
            elif i in self.PARRENT_TOPIC.values():
                temp_list.append(i)
            else:
                temp_list.append('Other')
        return ','.join(list(set(temp_list)))
                    
    def construct_df(self,df):
        df['parent_topic'] = df['topic_category'].apply(lambda x: self.parent_topic(x) if x is not None else None)
        df['parent_topic_primary'] = df['categoryId'].apply(lambda x: self.parent_topic_id(x) if x is not None else None)
        df['start_time(UTC)'].fillna(df['published_date'], inplace=True)
        df['day'] = df['start_time(UTC)'].dt.strftime('%A')
        df['hour'] = df['start_time(UTC)'].dt.strftime('%H')
        df['licensed_content'] = df['licensed_content'].astype(str)
        df['for_kids'] = df['for_kids'].astype(str)
        return df
    
    def construct_df_ML(self,df):
        #df['sub-topic'] = df['video_topic'].apply(lambda x: self.parent_topic(x) if x is not None else None)
        df['topic_primary'] = df['video_topic_id'].apply(lambda x: self.parent_topic_id(x) if x is not None else None)
        return df