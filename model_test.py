#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 15:12:23 2019

@author: smkj33
"""

import pymysql
from queries import *
from db_config import *

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer


import pandas as pd

def import_content ():

    try:
        conn = pymysql.connect(**connection_properties)
        sql = importContentQuery()
        df = pd.read_sql(sql, conn)

        #closing database connection.
        if(conn.open):
            conn.close()
            print("MySQL connection is closed")

        return df

    except Exception as e :
        print ("Error while connecting to MySQL", e)



def export_content(df):

    conn = pymysql.connect(**connection_properties)
    cursor = conn.cursor()

    try:
        sql = """
        INSERT INTO `recen_test` (`uid`, `json_col1`)
        VALUES(%s, %s)
        """
        df.apply(lambda row: cursor.execute(sql, (row.local_id, row.jsol_col1)), axis = 1)
        conn.commit()
    	# conn.commit()

        #closing database connection.
        if(conn.open):
            # conn.commit()
            conn.close()
            print("MySQL connection is closed")


    except Exception as e :
        print ("Error while connecting to MySQL", e)



# article_master = import_content()
# # article_master.apply(lambda x: print(x.to_json()), axis=1)
# df = pd.DataFrame(article_master.apply(lambda row: row.to_json(), axis=1), columns = ['jsol_col1'])
# df['local_id'] = df.index
# export_content(df)
# # print(df)



def export_map_1(df):
    sql = export_article_map_query()
    # """
    # INSERT INTO `recen_article_map` (`local_id`,`article_id`,`title`)
    # VALUES(%s, %s, %s)
    # """
    conn = pymysql.connect(**connection_properties)
    cursor = conn.cursor()
    # sql = export_article_map_query()

    try:
        df.apply(lambda row: cursor.execute(sql, (row.local_id, row.article_id, row.title )), axis = 1)
        conn.commit()

        #closing database connection.
        if(conn.open):
            conn.close()
            print("MySQL connection is closed")


    except Exception as e :
        print ("Error while connecting to MySQL", e)





# req = {'article_id': [1011,1019,1022],
#         'duration': [120,300,50]
#         }

# df = pd.DataFrame(req ,columns= ['article_id', 'duration'])

# print (df)






req = {'article_id': [1011, 1019, 1022], 'duration': [120, 300, 50]}
df = pd.DataFrame(req)
x = (get_local_id(df['article_id']))
# print(get_local_id(df['article_id']))
# print(get_similarity(get_local_id(df['article_id'])))
pd.set_option('max_colwidth', 10)
sim = get_similarity(x)


content_sim = sim['content_sim'].apply(lambda row: pd.read_json(row, typ = 'list'))
title_sim = sim['title_sim'].apply(lambda row: pd.read_json(row, typ = 'list'))
cat_tags_sim = sim['cat_tags_sim'].apply(lambda row: pd.read_json(row, typ = 'list'))


# print(content_sim)




# def text_soup_filter(text):
#     soup = BeautifulSoup(text, features="html5lib")
#     text = re.sub('[^a-z\s]', '',soup.get_text(separator=' ').lower())
#     return text



# article_master['reduced_content'] = article_master.apply(
#             lambda row: text_soup_filter(row.bodytext), axis = 1)


# article_master['reduced_content'] = article_master.apply(
#         lambda row: BeautifulSoup(row.bodytext).get_text().lower(), axis = 1)



# porter = PorterStemmer()
# def porter_stemmer (txt):
#     token_words=word_tokenize(txt)
#     stem_sentence=[]
#     for word in token_words:
#         stem_sentence.append(porter.stem(word))
#         stem_sentence.append(" ")
#     return "".join(stem_sentence)

# article_master['reduced_content_stemmed_nonum'] = article_master.apply(
#         lambda row: porter_stemmer(re.sub('[^a-z\s]', '',BeautifulSoup(row.bodytext).get_text(separator=' ').lower())), axis = 1)


# print(article_master)
















# from html.parser import HTMLParser


# # Strips HTML tags from text
# def strip_tags(html):
#     s = MLStripper()
#     s.feed(html)
#     # return s.get_data()
#     ret = ''.join([x.strip() for x in s.get_data().split('\r\n')])
#     return ret

# class MLStripper(HTMLParser):
#     def __init__(self):
#         self.reset()
#         self.strict = False
#         self.convert_charrefs= True
#         self.fed = []
#     def handle_data(self, d):
#         self.fed.append(d)
#     def get_data(self):
#         return ''.join(self.fed)



# def import_content ():
#     # user = 'root'
#     # password = 'log'
#     # db = 'db426841_843'
#     # host = '127.0.0.1'

#     # conn = pymysql.connect(host, user, password, db)
#     conn = pymysql.connect(**connection_properties)

#     cursor = conn.cursor()
    
#     try:
#         sql = importContentQuery()
#         cursor.execute(sql)
#         rows = cursor.fetchall()

#         for x in rows:
#             print("Id = ", x[0], )
#             print("Title = ", x[1])
#             print("Content  = ", strip_tags(x[2]))
#             # desired_string = ''.join([x.strip() for x in str(strip_tags(x[2])).split('\r\n')])
#             # print(desired_string )
#         cursor.close()
    
#     except Exception as e :
#         print ("Error while connecting to MySQL", e)
    
#     finally:
#         #closing database connection.
#         if(conn.open):
#             conn.close()
#             print("MySQL connection is closed")


